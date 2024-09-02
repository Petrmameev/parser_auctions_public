from apscheduler.schedulers.blocking import BlockingScheduler

from auctions import fetch_auction_data
from publichnoe_predlozhenie import fetch_pub_pred_data


def main():
    fetch_pub_pred_data(
        "https://m-ets.ru/search?q=eyJzZWFyY2hfY2F0ZWdvcnkiOiIyNyIsImlzcHViIjoib24iLCJ4cmVnaW9uW10iOlsiMjQiXX0",
        "Krasnoyarskiy_kray", "pub_pred_tovarno_materialnie_cennosti"
    )
    fetch_pub_pred_data(
        "https://m-ets.ru/search?q=eyJzZWFyY2hfY2F0ZWdvcnkiOiIxNSwxNiwxNywxOCwxOSwyMCwyMSwyMiwyMyIsImlzcHViIjoib24iLCJ4cmVnaW9uW10iOlsiMjQiXX0",
        "Krasnoyarskiy_kray", "pub_pred_oborudovanie"
    )
    fetch_pub_pred_data(
        "https://m-ets.ru/search?q=eyJzZWFyY2hfY2F0ZWdvcnkiOiIxMiwxMywxNCIsImlzcHViIjoib24iLCJ4cmVnaW9uW10iOlsiMjQiXX0",
        "Krasnoyarskiy_kray", "pub_pred_selskohozyaystvennoe_imushestvo"
    )
    fetch_pub_pred_data(
        "https://m-ets.ru/search?q=eyJzZWFyY2hfY2F0ZWdvcnkiOiIzMCIsImlzcHViIjoib24iLCJ4cmVnaW9uW10iOlsiMjQiXX0",
        "Krasnoyarskiy_kray", "pub_pred_prochee"
    )
    fetch_pub_pred_data(
        "https://m-ets.ru/search?q=eyJzZWFyY2hfY2F0ZWdvcnkiOiIyNCwyNSwyNiwyOSIsImlzcHViIjoib24iLCJ4cmVnaW9uW10iOlsiMjQiXX0",
        "Krasnoyarskiy_kray", "pub_pred_debitorskaya_zadolzhnost_i_cennie_bumagi"
    )
    fetch_pub_pred_data(
        "https://m-ets.ru/search?q=eyJzZWFyY2hfY2F0ZWdvcnkiOiIxLDMsNCw1LDYsMTIsOCIsImlzcHViIjoib24iLCJ4cmVnaW9uW10iOlsiMjQiXX0",
        "Krasnoyarskiy_kray", "pub_pred_avto_i_spectehnika"
    )
    fetch_pub_pred_data(
        "https://m-ets.ru/search?q=eyJzZWFyY2hfY2F0ZWdvcnkiOiIzNCwzNSwzNiwzOSIsImlzcHViIjoib24iLCJ4cmVnaW9uW10iOlsiMjQiXX0",
        "Krasnoyarskiy_kray", "pub_pred_nedvizhimost_dlya_lichnih_celey"
    )
    fetch_pub_pred_data(
        "https://m-ets.ru/search?q=eyJzZWFyY2hfY2F0ZWdvcnkiOiIzNywzOCwyOCIsImlzcHViIjoib24iLCJ4cmVnaW9uW10iOlsiMjQiXX0",
        "Krasnoyarskiy_kray", "pub_pred_nedvizhimost_dlya_biznesa"
    )
    fetch_pub_pred_data(
        "https://m-ets.ru/search?q=eyJzZWFyY2hfY2F0ZWdvcnkiOiIxMSIsImlzcHViIjoib24iLCJ4cmVnaW9uW10iOlsiMjQiXX0",
        "Krasnoyarskiy_kray", "pub_pred_zemelniye_uchastki"
    )

    fetch_auction_data(
        "https://m-ets.ru/search?q=eyJzZWFyY2hfY2F0ZWdvcnkiOiIyNyIsImlzYXVrIjoib24iLCJ4cmVnaW9uW10iOlsiMjQiXX0",
        "Krasnoyarskiy_kray", "auk_tovarno_materialnie_cennosti"
    )
    fetch_auction_data(
        "https://m-ets.ru/search?q=eyJzZWFyY2hfY2F0ZWdvcnkiOiIxNSwxNiwxNywxOCwxOSwyMCwyMSwyMiwyMyIsImlzYXVrIjoib24iLCJ4cmVnaW9uW10iOlsiMjQiXX0",
        "Krasnoyarskiy_kray", "auk_oborudovanie"
    )
    fetch_auction_data(
        "https://m-ets.ru/search?q=eyJzZWFyY2hfY2F0ZWdvcnkiOiIxMiwxMywxNCIsImlzYXVrIjoib24iLCJ4cmVnaW9uW10iOlsiMjQiXX0",
        "Krasnoyarskiy_kray", "auk_selskohozyaystvennoe_imushestvo"
    )
    fetch_auction_data(
        "https://m-ets.ru/search?q=eyJzZWFyY2hfY2F0ZWdvcnkiOiIzMCIsImlzYXVrIjoib24iLCJ4cmVnaW9uW10iOlsiMjQiXX0",
        "Krasnoyarskiy_kray", "auk_prochee"
    )
    fetch_auction_data(
        "https://m-ets.ru/search?q=eyJzZWFyY2hfY2F0ZWdvcnkiOiIyNCwyNSwyNiwyOSIsImlzYXVrIjoib24iLCJ4cmVnaW9uW10iOlsiMjQiXX0",
        "Krasnoyarskiy_kray", "auk_debitorskaya_zadolzhnost_i_cennie_bumagi"
    )
    fetch_auction_data(
        "https://m-ets.ru/search?q=eyJzZWFyY2hfY2F0ZWdvcnkiOiIxLDMsNCw1LDYsMTIsOCIsImlzYXVrIjoib24iLCJ4cmVnaW9uW10iOlsiMjQiXX0",
        "Krasnoyarskiy_kray", "auk_avto_i_spectehnika"
    )
    fetch_auction_data(
        "https://m-ets.ru/search?q=eyJzZWFyY2hfY2F0ZWdvcnkiOiIzNCwzNSwzNiwzOSIsImlzYXVrIjoib24iLCJ4cmVnaW9uW10iOlsiMjQiXX0",
        "Krasnoyarskiy_kray", "auk_nedvizhimost_dlya_lichnih_celey"
    )
    fetch_auction_data(
        "https://m-ets.ru/search?q=eyJzZWFyY2hfY2F0ZWdvcnkiOiIzNywzOCwyOCIsImlzYXVrIjoib24iLCJ4cmVnaW9uW10iOlsiMjQiXX0",
        "Krasnoyarskiy_kray", "auk_nedvizhimost_dlya_biznesa"
    )
    fetch_auction_data(
        "https://m-ets.ru/search?q=eyJzZWFyY2hfY2F0ZWdvcnkiOiIxMSIsImlzYXVrIjoib24iLCJ4cmVnaW9uW10iOlsiMjQiXX0",
        "Krasnoyarskiy_kray", "auk_zemelniye_uchastki"
    )

if __name__ == "__main__":
    main()


scheduler = BlockingScheduler()
scheduler.add_job(main, "interval", minutes=30)
scheduler.start()
