import requests
from django.core.paginator import Paginator
from django.shortcuts import render
import xml.etree.ElementTree as ET

def urun_listesi(request):
    url = "https://nalburxmlbayi.com/storage/cache/feed/0-nalbur.xml"
    response = requests.get(url)
    
    if response.status_code != 200:
        return render(request, 'urunler/urun_listesi.html', {'error': 'Veri alınamadı'})
    
    tree = ET.ElementTree(ET.fromstring(response.content))
    root = tree.getroot()

    urunler = []
    for item in root.findall('.//product'):
        urun = {
            'title': item.find('name').text if item.find('name') is not None else '',
            'link': '#',  # Eğer bir link yoksa placeholder kullanın
            'description': item.find('description').text if item.find('description') is not None else '',
            'price': item.find('price').text if item.find('price') is not None else '',
            'category': item.find('category').text if item.find('category') is not None else '',
            'sku': item.find('model').text if item.find('model') is not None else '',
            'image': item.find('image').text if item.find('image') is not None else ''
        }
        urunler.append(urun)

    # Arama işlemi
    query = request.GET.get('q')
    if query:
        urunler = [urun for urun in urunler if query.lower() in urun['title'].lower() or (urun['sku'] and query.lower() in urun['sku'].lower())]

    paginator = Paginator(urunler, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'urunler/urun_listesi.html', {'page_obj': page_obj, 'query': query})
