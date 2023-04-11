from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import httpx
from lxml import html
from getConfig import account, password, receiver_list, smtp_server, smtp_port
from jinja2 import Template
from datetime import datetime, timedelta
import sqlite3


class Item:
    def __init__(self, title, page_url, author, date):
        self.title: str = title
        self.page_url: str = page_url
        self.author: str = author
        self.date: datetime.date = date

    def values(self):
        return [self.title, self.page_url, self.author, self.date]


def get_lastest_10_oa():
    url: str = "http://oa.stu.edu.cn/csweb/list.jsp?pageindex=1"
    r = httpx.get(url)
    html_code: str = r.text
    r.close()

    tree = html.fromstring(html_code)

    lines = tree.xpath("/html/body/div/form/table/tbody[1]/tr")
    items = []

    # 提取出单独的条目，跳过第一条（表头）
    for i, line in enumerate(lines):
        if i == 0:
            pass
        else:
            title = line.xpath("td[1]/a/@title")[0]
            page_url = "http://oa.stu.edu.cn" + line.xpath("td[1]/a/@href")[0]
            author = line.xpath("td[2]/text()")[0]
            date = str_to_date(line.xpath("td[3]/text()")[0])
            # item = {
            #     "title":title,
            #     "page_url":page_url,
            #     "author":author,
            #     "date":date
            # }
            item = Item(title, page_url, author, date)
            items.append(item)
    return items


def str_to_date(date_str):
    return datetime.strptime(date_str, "%Y-%m-%d").date()


def insert_item_into_db(item: Item) -> bool:
    with sqlite3.connect("oa.db") as db:
        cursor = db.cursor()
        if bool(query_from_db(item)):
            print(f"already exists:\t{item.title}")
            return False
        else:
            sql = "insert into oa_items(title,page_url,author,date) values(?,?,?,?)"
            cursor.execute(sql, item.values())
            db.commit()
            return True


def query_from_db(item: Item):
    with sqlite3.connect("oa.db") as db:
        cursor = db.cursor()
        sql = "select * from oa_items where title=?"
        cursor.execute(sql, (item.title,))
        result = cursor.fetchall()

    return result


def del_old_then_one_week_item():
    the_last_week_date = str(datetime.today().date() - timedelta(days=7))
    with sqlite3.connect("oa.db") as db:
        cursor = db.cursor()
        sql = "delete from oa_items where date=?"
        cursor.execute(sql, (the_last_week_date,))
        db.commit()


def gen_mail_content(items: list):
    template = Template(open("template.html").read())

    return template.render(items=items)


def send_email(to, subject, body, account, password):
    """
    发送邮件，
    这段代码完全是从ChatGPT哪里抄来的，便不添注释了（。。。）
    """

    # Create message container
    msg = MIMEMultipart()
    msg["From"] = account
    msg["To"] = ", ".join(to)
    msg["Subject"] = subject

    # Add body to email
    body = MIMEText(body, "html")
    msg.attach(body)

    # Send email using SMTP
    with smtplib.SMTP(smtp_server, smtp_port) as smtp:
        smtp.starttls()
        smtp.login(account, password)
        smtp.send_message(msg)


def oa_helper():
    items = get_lastest_10_oa()
    dateline = datetime.strptime("2023-4-2", "%Y-%m-%d").date()
    new_items = []
    for item in items:
        is_new = insert_item_into_db(item)
        if is_new:
            new_items.append(item)
    if len(new_items) > 0:
        email_content = gen_mail_content(new_items)
        try:
            send_email(receiver_list, "OA Helper", email_content, account, password)
        except Exception as e:
            print(e)
        print(email_content)
    del_old_then_one_week_item()


if __name__ == "__main__":
    oa_helper()
