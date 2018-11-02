import requests
from bs4 import BeautifulSoup
from logging import getLogger
import json

LOG = getLogger(__name__)


def main(name, roll_no, room_no, form_id, default_option):
    """

    :param name:
    :param roll_no:
    :param room_no:
    :param form_id:
    :param default_option:
    :return:
    """
    form_url = "https://docs.google.com/forms/d/e/"+form_id+"/formResponse"

    sess = requests.Session()
    resp = sess.get(form_url)
    # print(resp.status_code)
    if resp.status_code != 200:
        LOG.error("Not valid form ID")
        return False

    # print(resp.content)
    resp = BeautifulSoup(resp.content, "html.parser")
    scripts = resp.find_all("script")

    final_script = ""
    for script in scripts:
        if "FB_PUBLIC_LOAD_DATA" in script.text:
            final_script = script
            break
    # print(final_script)

    first_cut = 0
    last_cut = 0
    for ind, val in enumerate(final_script.text):
        if val == "[":
            if first_cut == 0:
                first_cut = ind
        elif val == "]":
            last_cut = ind

    # print(first_cut, last_cut)
    final_script = final_script.text[first_cut:last_cut+1]
    # print(final_script)

    entry_list = json.loads(final_script)
    # print(entry_list[1][1])
    entry_list = entry_list[1][1]

    # print(entry_list)

    count = 0

    user_agent = {
        'Referer': form_url,
        'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36"
    }

    entry_dict = {
        'fvv': 1,
        'pageHistory': "0,1"
    }

    for x in range(1, len(entry_list)):
        count = count + 1
        item = entry_list[x]
        print(item)
        item = item[len(item)-1]
        for each in item:
            # print(each[0])
            each = str(each[0])
            if count == 1:
                entry_dict['entry.'+each] = name
            elif count == 2:
                entry_dict['entry.'+each] = roll_no
            elif count == 3:
                entry_dict['entry.'+each] = room_no
            else:
                entry_dict['entry.'+each] = default_option

    requests.post(form_url, data=entry_dict, headers=user_agent)
    return True


if __name__ == "__main__":
    name = input("Enter your name: ")
    roll_no = input("Enter your roll no: ")
    room_no = input("Enter your room no: ")
    form_id = input("Enter the form ID: ")
    default_option = input("Enter the option you want to mark: ")

    main(name, roll_no, room_no, form_id, default_option)
    # main()
