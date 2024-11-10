import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime

doviz={
   'com' : 'USD',
   'co.uk' : 'GBP',
   'ca' : 'CAD',
   'fr' : 'EUR',
   'de' : 'EUR',
   'se' : 'SEK'
   
}


def exchangeapi(from_currency, to_currency):
   apiurl=f"https://raw.githubusercontent.com/WoXy-Sensei/currency-api/main/api/{from_currency}_{to_currency}.json"
   
   header = {"accept-language": "en-US,en;q=0.9","accept-encoding": "gzip, deflate, br","User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36","accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7"}
   
   request = requests.get(apiurl, headers=header)

   if request.status_code == 200:
        data = request.json()
        if 'rate' in data:
            return data['rate']
        else:
           print("API'den bilgi alınamadı...")
           return None
    
   else:
        print(f"Hata oluştu: {request.status_code}")
        return None

def exchange(miktar,donusturulen,donusturulecek):
   dovizkuru =exchangeapi(donusturulen, donusturulecek)
   if dovizkuru is not None:
      islem = miktar* dovizkuru
      return islem
   else: 
      print("döviz kuru alınamadı")
      return None

def fiyatalma(url):
   o={}

   header = {"accept-language": "en-US,en;q=0.9","accept-encoding": "gzip, deflate, br","User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36","accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7"}
   
   resp = requests.get(url, headers=header)
   print(resp.status_code)
   
   if(resp.status_code != 200):
      print(resp)
      
   soup=BeautifulSoup(resp.text,'html.parser')
   
   try:
      pricestring =soup.find("span",{"class":"a-price"}).find("span").text
      price = float(re.sub(r'[^\d.]', '', pricestring))
      return price
      
   except Exception as e:
      print(f"fiyat bulunamadı...: {e}")
      return None

def id_suffix_alma(url):
   patern = r'/dp/([A-Z0-9]+)'
   match = re.search(patern,url)
   if match:
      productid = match.group(1)
      suffix = ""
      return productid, suffix
   else:
      print("geçersiz amazon URL'si.  ")
      return None, None

def dinamikurl(productid, suffix, countrycode="com" ):
   baseurl = f"https://www.amazon.{countrycode}/dp/{productid}{suffix}"
   return baseurl



print(""" 
                      --ADIMLAR--
1- Dinamik URL elde edebilmek için ürünün linkini giriniz.

2- Fiyatı görmek istediğiniz PAZARI seçin.

3- Fiyatı görmek istediğiniz KUR BAZINI seçin.
""")


url = input("Bir Amazon ürün linki giriniz:  ").strip()
productid, suffix=id_suffix_alma(url=url)

if not productid:
   print("Ürün ID'si bulunamadı")
   exit()

print("""
   **ÜLKE KODLARI**
   US      = "com"
   UK      = "co.uk"
   CANADA  = "ca"
   FRANCE  = "fr"
   GERMANY = "de"
   SWEDEN  = "se"

""")
countrycode = input("Fiyatı görmek istediğiniz pazarı seçin:  ").strip().lower()


if(countrycode in doviz ):
   donusturulen = doviz[countrycode]
else:
   print("Geçersiz ulke kodu")
   exit()
   
print("""
   **KUR BAZLARI**
   USD - Amerikan Doları
   EUR - Euro
   CAD - Kanada Doları
   SEK - İsveç Kronu
   GBP - İngiliz Sterlini
""")

donusturulucek = input("Fiyatı görmek istediğiniz kur bazını seçin :  ").strip().upper()

urldnmc = dinamikurl(productid,suffix,countrycode)
print("Dinamik Url: ",urldnmc)

fiyat = fiyatalma(urldnmc)

if fiyat:
   donusturulmusfiyat = exchange(fiyat, donusturulen, donusturulucek)
   if donusturulmusfiyat:
      print(f'Ürünün seçtiğiniz pazardaki fiyati: {donusturulmusfiyat} {donusturulucek}')
   else:
      print("Döviz dönüsümü yapilamadi...")
else:
   print("Fiyat bulunamadı...")

