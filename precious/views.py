from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import user_passes_test
import json
from precious import models, asset_handler


# Create your views here.


@csrf_exempt
def report(request):
    if request.method == 'POST':
        asset_data = request.POST.get('asset_data')
        data = json.loads(asset_data)
        if not data:
            return HttpResponse("没有数据！")
        if not issubclass(dict, type(data)):
            return HttpResponse("数据必须为字典格式！")
        sn = data.get('sn', None)
        if sn:
            asset_obj = models.Asset.objects.filter(sn=sn)
            if asset_obj:
                update_asset = asset_handler.UpdateAsset(request, asset_obj[0], data)
                return HttpResponse("资产数据已更新！")
            else:
                obj = asset_handler.NewAsset(request, data)
                response = obj.add_to_new_assets_zone()
                return HttpResponse(response)
        else:
            return HttpResponse("没有资产sn序列号， 请检查数据！")
    return HttpResponse('200 ok')


@user_passes_test(lambda u: u.is_superuser)
def index(request):
    assets = models.Asset.objects.all()
    return render(request, 'precious/index.html', locals())


@user_passes_test(lambda u: u.is_superuser)
def dashboard(request):
    total = models.Asset.objects.count()
    online = models.Asset.objects.filter(status=0).count()
    offline = models.Asset.objects.filter(status=1).count()
    unknown = models.Asset.objects.filter(status=2).count()
    breakdown = models.Asset.objects.filter(status=3).count()
    backup = models.Asset.objects.filter(status=4).count()

    up_rate = round(online / total * 100)
    o_rate = round(offline / total * 100)
    un_rate = round(unknown / total * 100)
    bd_rate = round(breakdown / total * 100)
    bu_rate = round(backup / total * 100)

    server_number = models.Server.objects.count()
    networkdevice_number = models.NetworkDevice.objects.count()
    memorydevice_number = models.MemoryDevice.objects.count()
    securitydevice_number = models.SecurityDevice.objects.count()
    software_number = models.Software.objects.count()

    return render(request, 'precious/dashboard.html', locals())


@user_passes_test(lambda u: u.is_superuser)
def detail(request, asset_id):
    asset = get_object_or_404(models.Asset, id=asset_id)
    return render(request, 'precious/detail.html', locals())
