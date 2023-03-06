import module_5 as m5
# Press the green button in the gutter to run the script.
if __name__ == "__main__":

    stop = False

    while not stop:
        input_info_format = input(f"Select input source:\n1 - Manual input from console\n2 - From file\n")
        if input_info_format == "1":
            input_handler = m5.InputManualHandler(input_info_format)
            publication_type_in = input_handler.get_pub_type()
            if publication_type_in == "1":
                publication_name_in = input_handler.get_pub_name(publication_type_in)
                publication_city_in = input_handler.get_city()
                publication_text_in = input_handler.get_text()
                news_provider = m5.NewsFeedProvider(publication_name_in, publication_city_in, publication_text_in)
                feed = m5.Publication(handler=m5.ConcreteFileHandler("feed.txt"),
                                      provider=news_provider)
            if publication_type_in == "2":
                publication_name_in = input_handler.get_pub_name(publication_type_in)
                publication_text_in = input_handler.get_text()
                publication_exp_date_in = input_handler.get_exp_date()
                adv_provider = m5.AdvFeedProvider(publication_name_in, publication_text_in, publication_exp_date_in)
                feed = m5.Publication(handler=m5.ConcreteFileHandler("feed.txt"),
                                      provider=adv_provider)
            if publication_type_in == "3":
                publication_name_in = input_handler.get_pub_name(publication_type_in)
                publication_city_in = input_handler.get_city()
                publication_text_in = input_handler.get_text()
                publication_exp_date_in = input_handler.get_exp_date()
                publication_discount_in = input_handler.get_discount()
                disc_provider = m5.DiscountFeedProvider(publication_name_in, publication_city_in,
                                                        publication_text_in, publication_exp_date_in,
                                                        publication_discount_in)
                feed = m5.Publication(handler=m5.ConcreteFileHandler("feed.txt"),
                                      provider=disc_provider)
            # try:
            #     feed.publish()
            # except TypeError as te:
            #     print(f"Feed cannot be published due to {te}")
            feed.publish()



