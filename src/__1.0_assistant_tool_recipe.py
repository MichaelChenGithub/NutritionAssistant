from bs4 import BeautifulSoup
import requests

def find_method_step(soup, recipe_detail):
    h3_text = "Method"
    h3 = soup.find("h3", string=h3_text)
    if h3:
        # 檢查 h3 的父層是否是具有特定 class 的元素
        parent_section = h3.find_parent("section", class_="recipe__method-steps")
        if parent_section:
            for element in parent_section:
                recipe_detail += element.text
        else:
            recipe_detail += "Can't found the recipe method."
    else:
        recipe_detail += "Can't found the recipe method."
    return recipe_detail

def find_ingredients(soup, recipe_detail):
    h2_text = "Ingredients"
    h2 = soup.find("h2", string=h2_text)
    if h2:
        # 檢查 h2 的父層是否是具有特定 class 的元素
        parent_section = h2.find_parent("section", class_="recipe__ingredients")
        if parent_section:
            for element in parent_section:
                recipe_detail += element.text
        else:
            recipe_detail += "Can't found the ingredient element."
    else:
        recipe_detail += "Can't found the ingredient element."
    return recipe_detail

def find_nutrition(soup, recipe_detail):
    # find nutrition information
    caption_text_partial = "Nutrition: per"
    caption = soup.find("caption", string=lambda text: text and caption_text_partial.lower() in text.lower())
    if caption:
        table = caption.find_parent("table")
        # find nutrition table
        if table:
            # Do something with the table
            for element in table:
                recipe_detail += element.text
        else:
            recipe_detail += ("Can't found the nutrition information.")
    else:
        recipe_detail += ("Can't found the nutrition information.")
    return recipe_detail

def recipe_scraper(headers, link):
    recipe_detail = ""
    # find recipe webpage
    webpage = requests.get(f"https://www.bbcgoodfood.com{link}" ,headers=headers)
    soup = BeautifulSoup(webpage.content)

    # find ingredient element
    recipe_detail += find_ingredients(soup, recipe_detail)
    recipe_detail += "|"
    
    # find method step
    recipe_detail += find_method_step(soup, recipe_detail)
    recipe_detail += "|"

    # find nutrition
    recipe_detail += find_nutrition(soup, recipe_detail)
    
    return recipe_detail

def get_recipe(query):
    headers = {"User-agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36"}
    recipe_list_page = requests.get(f'https://www.bbcgoodfood.com/search?q={query}' ,headers=headers)
    recipe_list_soup = BeautifulSoup(recipe_list_page.content)

    result = ""
    for article in recipe_list_soup.find_all("article")[:1]:
        recipe_info = "".join([article["data-item-name"], ":"])
        try:
            link = article.find("a")["href"]
            recipe_info += recipe_scraper(headers, link)
        except KeyError as e:
            recipe_info += recipe_info.join("Can't find recipe information.")
        result += recipe_info
    return result