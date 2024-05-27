import time
import os
from discord_webhook import DiscordWebhook, DiscordEmbed
from pyVinted import Vinted
from typing import List
from requests.exceptions import HTTPError
import utils
import json
import requests
import re
import random
from requests.exceptions import HTTPError
from datetime import datetime

WEBHOOK_URL = "https://discord.com/api/webhooks/1159600575307055164/HLbqVnwEOc18RioqPpRaeQdId5GLfx6E1FzvKPGFxw_FQi4WzINZLgsAvltjQi6W538p"

os.system("title Wallapop Scraping $_$ By Sergi")

banner = """
            **       **            **  **                                   
/**      /**           /** /**           ******           ****** 
/**   *  /**  ******   /** /**  ******  /**///**  ****** /**///**
/**  *** /** //////**  /** /** //////** /**  /** **////**/**  /**
/** **/**/**  *******  /** /**  ******* /****** /**   /**/****** 
/**** //**** **////**  /** /** **////** /**///  /**   /**/**///  
/**/   ///**//******** *** ***//********/**     //****** /**     
//       //  //////// /// ///  //////// //       //////  //  

                🤑 Wallapop Bot v1
                    By Sergi

""".replace("$", utils.PURPLE + "$" + utils.WHITE).replace("_", utils.RED + "_" + utils.WHITE).replace("|", utils.RED + "|" + utils.WHITE).replace("/", utils.RED + "/" + utils.WHITE).replace("\\", utils.RED + "\\" + utils.WHITE)
print(banner)

last_item_id = ""
sent_items = []
MAX_RETRIES = 3
# allowed_brands = ["nike", "adidas", "ralph lauren", "puma"] # list of brands you want
allowed_country_code = "fr" # your country
allowed_price = 200 # your max price
producto = "camiseta-barcelona"
URL = "https://es.wallapop.com/item/"
HEADERS = {
            "User-Agent": "PostmanRuntime/7.28.4",  # random.choice(USER_AGENTS),
            "Accept": "*/*",
}
contador= 0
while True:
    try:
        time.sleep(120)    
        vinted = Vinted()
        items = search("https://api.wallapop.com/api/v3/general/search?keywords="+producto+"&order_by=newest")
        items_ordenados = sorted(items, key=lambda x: x.date)
        ultimos_10_items = items_ordenados[-5:]
        for item in ultimos_10_items:
            # if item.brand_title.lower() in allowed_brands:
                if item.id not in sent_items: 
                    sent_items.append(item.id)  
                    contador += 1
                    titler = item.title if item.title else "Not found"
                    screen = item.photo if item.photo else "Not found"
                    # brand = item.brand_title if item.brand_title else "Not found"
                    price = f"{item.price}€" if item.price else "Not found"
                    url = item.url if item.url else "Not found"


                    fecha = datetime.fromisoformat(item.date)
                    fecha_formateada = fecha.strftime("%Y-%m-%d %H:%M:%S")
                    # create = item.created_at_ts.strftime("%Y-%m-%d %H:%M:%S") if item.created_at_ts else "Not found"

                    webhook = DiscordWebhook(url=WEBHOOK_URL)
                    embed = DiscordEmbed(title="", description=f"**[{titler}]({url})**", color=3447003)
                    embed.add_embed_field(name="", value="", inline=False)
                    embed.set_thumbnail(url="https://media.vandalsports.com/i/1706x960/12-2023/20231230184511_1.jpg?resize=500,432")
                    embed.set_image(url=screen)
                    embed.add_embed_field(name="⌛ Publication", value=contador, inline=True)
                    # embed.add_embed_field(name="🔖 Marque", value="0", inline=True)
                    embed.add_embed_field(name="💰 Prcio", value=price, inline=True)
                    embed.add_embed_field(name="📆 Fecha", value=fecha_formateada, inline=True)
                    # embed.set_description(item.description)
                    embed.set_footer(text="Bot Vinted by Sergi")
                    webhook.add_embed(embed)
                    response = webhook.execute()

                    if response.status_code == 200:
                        print('[+] Embed sent successfully.')
                    else:
                        print('[-] Failed to send embed. Status code:', response.status_code)

                else:
                    print("[INFO] Already shown ")

    except Exception as e:
        print("[INFO] Failed:", str(e))

    def search(url, nbrItems: int = 20, page: int =1, time: int = None, json: bool = False):
            try:

                response = get(url=url)
               
                response.raise_for_status()
                
                items = response.json()
                items = response.json()["search_objects"]
                
                if not json:
                    return [Item(_item) for _item in items]
                else:
                    return items

            except HTTPError as err:
             raise err
            
    def get(url):
        """
        Perform a http get request.
        :param url: str
        :param params: dict, optional
        :return: dict
            Json format
        """
        tried = 0
        session = requests.Session()
        session.headers.update(HEADERS)  
        while tried < MAX_RETRIES:
            tried += 1
            with session.get(url) as response:

                if response.status_code == 401 and tried < MAX_RETRIES:
                    print(f"Cokkies invalid retrying {tried}/{MAX_RETRIES}")
                    

                elif response.status_code == 200 or tried == MAX_RETRIES:
                    return response


        return HTTPError
    class Item:
        def __init__(self, data):
            self.raw_data = data
            self.id = data["id"]
            self.title = data["title"]
            self.description = data["description"]
            self.currency = data["currency"]
            self.price = data["price"]
            self.photo = data["images"][0]["small"]
            self.date = data["modification_date"]
            self.url = URL+data["web_slug"]
            
      