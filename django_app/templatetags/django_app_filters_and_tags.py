from django import template
from django_app import models
import requests
import bs4

register = template.Library()


@register.filter(name="custom_cut")
def custom_cut(text: any, length: int) -> str:
    if len(str(text)) > length:
        return str(text)[:length] + "..."
    return str(text)


@register.filter(name="digitize_num")
def digitize_num(num: int) -> str:
    return "{0:,}".format(num).replace(",", " ")


@register.simple_tag
def comment_count(article_id: str) -> int:
    count = models.CommentItem.objects.filter(
        article__id=article_id, is_active=True
    ).count()
    return count


@register.simple_tag
def item_rating(item_id: str) -> int:
    _item = models.Item.objects.get(id=int(item_id))
    _ratings = models.ItemRating.objects.all().filter(item=_item)
    return (
        _ratings.filter(is_like=True).count() - _ratings.filter(is_like=False).count()
    )


@register.simple_tag
def get_temp(city):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_2 like Mac OS X; nl-nl) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8H7 Safari/6533.18.5",
            "Referer": "https://yandex.kz/",
            "Accept-Language": "en-US,en;q=0.5",
        }

        res = requests.get(f"https://pogoda.co.il/kazakhstan/{city}", headers=headers)
        res.raise_for_status()

        weather_soup = bs4.BeautifulSoup(res.text, "html.parser")

        temp = weather_soup.find("strong").get_text(strip=True)

        return temp

    except requests.RequestException as e:
        return "Error fetching temperature"

    except Exception as e:
        return "Error fetching temperature"
