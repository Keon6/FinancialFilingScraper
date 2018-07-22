
# TASKS:
# 1. FIX the code so that EquityData() object gives financial data for the last x years
from selenium import webdriver
from bs4 import BeautifulSoup
from googlefinance import getQuotes
from pandas_datareader import data
import csv
import collections
import urllib.request
dir(urllib.request)

'''
DOCUMENTATION:
This file contains all Objects that has to deal with reading and sorting financial files.
Such files include historical stock prices, and financial filings like 10-K and 10-Q.
An object that creates CSV file also exists.

__authors__ = ["Keon Shik (Kevin) Kim"]
__contributors__ = [""]
__credits__ = ["Keon Shik (Kevin) Kim"]

__version__ = 0.0.2
__maintainers__ = ["Keon Shik (Kevin) Kim"]
__email__ = ["kevinkim1207@gmail.com"]
'''




#PROBLEM: RUNNIG TIME IS TOO LONG


def html_to_text(html):
    """ Converts HTML list to text list
    O(n)
    :param html: HTML list
    :return: text list, initially empty
    """
    text = list()
    for i in range(0, len(html)):
        text.append(html[i].get_text())
    return text


def has_numb(inputs):
    """ Checks whether a given input has a number or not
    O(1)
    :param inputs: element in a list
    :return: boolean that tells whether inputs is a number or not
    """
    is_numb = True
    if inputs.find("1") == -1 and inputs.find("2") == -1 and inputs.find("3") == -1 and inputs.find("4") == -1\
            and inputs.find("5") == -1 and inputs.find("6") == -1 and inputs.find("7") == -1 \
            and inputs.find("8") == -1 and inputs.find("9") == -1 and inputs.find("0") == -1:
        is_numb = False
    return is_numb


def rabin_karp_multiple_pattern_search(string, substring_list):
    """
    Assumes that all substrings have the same length
    :param string:
    :param substring_list:
    :return:
    """
    hashed_substring_list = set()
    m = len(substring_list[0])
    for sub in substring_list:
        hashed_substring_list.add(hash(sub[:m]))
    hs = hash(string[:m])
    # print(hs)
    for i in range(len(string)-m+1):
        if hs in hashed_substring_list and string[i:i+m] in substring_list:
            return i
        hs = hash(string[i+1:i+m+1])
    return -1

#WORK OM IT
def remove_item(substring_list, string_list, self_or_not): #WORK an SORTING SO THAT I COULD IMPLEMENT BINARY SEEARCH
    """ Goes through a list and removes any element that contains the given substring

    :param substring_list: If the string contains the following substring, then remove it
    :param string_list: List we want to go through
    :param self_or_not: If substring == string, then False. If substring is contained, then True.
    :return:
    """

    for string in string_list:
        if rabin_karp_multiple_pattern_search(string, substring_list) != 1:
            string_list.pop(string)


    counter = 0
    back_counter = len(string_list)
    while counter < back_counter:
        if self_or_not is True:
            if string_list[counter].find(substring_list) != -1:
                string_list.pop(counter)
                back_counter = back_counter - 1
            else:
                counter = counter + 1
        else:
            if string_list[counter] == substring_list:
                string_list.pop(counter)
                back_counter = back_counter - 1
            else:
                counter = counter + 1


def remove_item_ranged(substring, li, rng):#WORK an SORTING SO THAT I COULD IMPLEMENT BINARY SEEARCH
    """ Similar to remove_item(), but it removes the given item if the substring falls in that range
    :param substring:
    :param li: list
    :param rng: given range
    :return:
    """
    counter = 0
    back_counter = len(li)
    while counter < back_counter:
        if li[counter].find(substring) == rng:
            li.pop(counter)
            back_counter = back_counter-1
        else:
            counter = counter + 1


def remove_if_failed(l, condition): #WORK an SORTING SO THAT I COULD IMPLEMENT BINARY SEEARCH
    """ remove items from a list that does not meet the given condition
    :param l: list
    :param condition: boolean that describes if a given condition is True or False
    :return:
    """
    counter = 0
    back_counter = len(l)
    while counter < back_counter:
        if condition is False:
            l.pop(counter)
            back_counter = back_counter - 1
        else:
            counter = counter + 1


def move_item(substring, self_or_not, li1):
    """ Similar to remove_item, but if a given substring is contained, then add li[i] to li2
    :param substring:
    :param self_or_not: If substring == string, then False. If substring is contained, then True.
    :param li1: List being searched
    :return: li2, List being added
    """
    li2 = list()
    if self_or_not is True:
        counter = 0
        back_counter = len(li1)
        while counter < back_counter:
            if li1[counter].find(substring) == 0:
                li2.append(li1[counter])
                back_counter = back_counter - 1
            counter = counter + 1
    elif self_or_not is False:
        while substring in li1:
            li2.append(substring)
    return li2
    # String inside f should be replaced with some visual interface eventually
    # parse_html = html.find_all("tr")
    # names_html = html.find_all("div", style="text-align:left;font-size:10pt;")
    # let's put on some action
    # wanted_data = html_to_text(parse_html)
    # names = html_to_text(names_html)


def create_csv(file, loc):
    """ creates csv file
    :param file: data we want to make into csv file
    :param loc: location to store the file
    :return:
    """
    file.to_csv(loc)


class EquityData:
    """
    This Class is an Object for Financial Files of public companies and Historical Stock Prices.
    Inputs: url_initial, ticker, period (length of time), time_frame (Type in '10-K' or '10-Q')
    Additionally, the class has a function that can remove all the unnecessary data from line-parsed text
    NOTE: ticker should be in all lower case
    NOTE: For period, choose 10, 20, 40, 80, or 100
    """
    def __init__(self, ticker, document_type, period):
        """

        :param ticker: String - Stock Ticker
        :param document_type: String = '10-Q' for quarterly filings or '10-K' for annual filing
        :param period: Int - Number of time periods
        """
        # Sanity checks first
        if ticker is not str:
            raise TypeError("ticker should be a String")
        if document_type != '10-Q' and document_type != '10-K':
            raise ValueError("document_type should be either '10-Q' or '10-K'")
        if period not in [10, 20, 40, 80, 100]:
            raise ValueError("For period, choose among numbers 10, 20, 40, 80, 100")

        self._ticker = ticker
        self._document_type = document_type
        self._periods_available = period

        self._html_list = collections.deque()
        self._line_html_list = collections.deque()
        self._text_list = collections.deque()
        self.money_scale_list = list()  # stores money scale data
        self.wanted_data = dict()
        self.url_filing_list = dict()

    def _extract_transform_load(self):
        """
        Scrape data from SEC.gov
        :return:
        """
        driver = webdriver.PhantomJS("C:\\Users\\kevin\\Downloads\\phantomjs-2.1.1-windows\\bin\\phantomjs.exe")
        driver.get(f"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={self._ticker}"
                   f"&type={self._document_type}&dateb=&owner=exclude&count={self._periods_available}")
        document_buttons = driver.find_elements_by_id("documentsbutton")
        self._periods_available = len(document_buttons)

        for i in range(self._periods_available):
            document_buttons = driver.find_elements_by_id("documentsbutton")
            document_buttons[i].click()
            if self._document_type == "10-Q":
                # Extract
                driver.find_element_by_partial_link_text("q.htm").click()
                url = driver.current_url
                # self.url_filing_list["YYYY - Q" + str(i)] = url #change the name of course
                soup = BeautifulSoup(urllib.request.urlopen(url), "html.parser")
                html = soup.prettify()
                line_html = soup.find_all("tr")
                text = html_to_text(line_html)
                # Transform
                self.clean(text)
                # Load
                self._html_list.append(html)
                self._line_html_list.append(line_html)
                self.money_scale_list.append(self.money_scale(html))
                self._text_list.append(text)
            if self._document_type == "10-K":
                # Extract
                driver.find_element_by_partial_link_text("k.htm").click()
                url = driver.current_url
                # self.url_filing_list["Y?" + str(i)] = url #change the name of course
                soup = BeautifulSoup(urllib.request.urlopen(url), "html.parser")
                html = soup.prettify()
                line_html = soup.find_all("tr")
                text = html_to_text(line_html)
                # Transform
                self.clean(text)
                # Load
                self._html_list.append(html)
                self._line_html_list.append(line_html)
                self.money_scale_list.append(self.money_scale(html))
                self._text_list.append(text)
            driver.back()
            driver.back()

    @property
    def current_price(self):
        return getQuotes(self._ticker)

    @property
    def ticker(self):
        return self._ticker

    @property
    def document_type(self):
        return self._document_type

    @property
    def load_data(self):
        return self.wanted_data

    def get_url_filing_list(self):
        return self.url_filing_list

    def get_period_available(self):
        return self._periods_available

    def historical_data(self, source, start):
        """ return historical data in a given time frame
        Time frame formats are YYYY-MM-DD
        :param source: string, is the data from Google-Finance or Yahoo-Finance
        :param start: starting time
        :return: list of historical data
        """
        return data.DataReader(self._ticker, source, start)

    #WORK ON THIS
    @staticmethod
    def money_scale(html):
        # O(n)
        """ This function checks if the reported dollar amounts are in thousands or in millions.
        In each report it says either 'dollars in millions' or 'dollars in thousands'
        NOTE: ALWAYS CALL BEFORE PRETTIFY()
        :return: String saying thousands or millions of dollars in scale
        """
        for i in range(0, len(html) - 10000):
            if (html[i] == 'n' and html[i + 3] == 'i' and html[i + 5] == 'l' and html[i + 7] == 'o'
                and html[i + 9] == 's') \
                    or (html[i] == 'i' and html[i + 2] == 'l' and html[i + 4] == 'o'
                        and html[i + 6] == 's' and html[i + 12] == 'o' and html[i + 14] == 'l'
                        and html[i + 16] == 'r'):
                return "Dollars in Millions"
            if (html[i] == 'n' and html[i + 3] == 'h' and html[i + 5] == 'u' and html[i + 7] == 'a'
                and html[i + 9] == 'd') \
                    or (html[i] == 'h' and html[i + 2] == 'u' and html[i + 4] == 'a'
                        and html[i + 6] == 'd' and html[i + 13] == 'o' and html[i + 15] == 'l'
                        and html[i + 17] == 'r'):
                return "Dollars in Thousands"

    #WORK ON THIS
    @staticmethod
    def clean(text_file):
        #O(n)
        """ This function should remove unnecessary elements and standardize the format of all financial files
        NOTE: DON"T CALL THIS BEFORE CALLING money_scale()
        :return:
        """
        c = 0
        bc = len(text_file)
        while c < bc:
            if has_numb(text_file[c]) is False:
                text_file.pop(c)
                bc = bc - 1
            elif has_numb(text_file[c][0]) is True:
                text_file.pop(c)
                bc = bc - 1
            else:
                c = c + 1
        substring_list = ['Delaware', 'California', 'January', 'February', 'March', 'April', 'May', 'June', 'July',
                          'August', 'September', 'October', 'November', 'December', 'PART', 'ITEM', 'Item', 'XBRL',
                          'Quarter Ended', 'Statements', 'Sheets', 'Page', 'CommonStock', 'Exhibit', 'Date', '●', '•',
                          'Section', 'Agreement', 'Bylaw', 'Form', 'Rule', 'Note', 'SIGNATURE', 'Emerging', 'Glossary',
                          'Summary', 'Events', 'Supplemental', 'Business', 'QUARTERLY', 'INDEX', 'SECURITIES EXCHANGE',
                          'Standard & Poor’s', 'Moody’s']
        remove_item
        remove_item_ranged('', text_file, 0)
        remove_item_ranged('Consolidated', text_file, 0)

    def insert_into_dict(self, w, text_file): #May be use sorting to decreas time complexity
        for i in range(0, len(text_file)):
            if text_file[i].find(w) == 0:
                # Case 1: with $
                if text_file[i][len(w)].find('$') != -1 or text_file[i][len(w) + 1].find('$') != -1:
                    temp = text_file[i]
                    print("----------------")
                    print("CASE 1")
                    print(temp)
                    temp = temp.replace(w, '')
                    print(temp)
                    rng = temp.find('$')
                    temp = temp[rng + 1:]
                    print(temp)
                    rng = temp.find('$')
                    temp = temp[0:rng]
                    print(temp)
                    temp = temp.replace(',', '')
                    temp = temp.replace('$', '')
                    temp = temp.replace('(', '-')
                    temp = temp.replace(')', '')
                    print(temp)
                    print("----------------")
                    self.wanted_data[w] = float(temp)
                    break
                # Case 2: numbers only, indentation in the middle
                if text_file[i][len(w) + 1:].find(' ') != -1:
                    # Case 2a: "xxx yyy"
                    if has_numb(text_file[i][len(w)]) is True and text_file[i][len(w):].find('$') == -1:
                        temp = text_file[i]
                        print("----------------")
                        print("CASE 2a")
                        print(temp)
                        temp = temp.replace(w, '')
                        print(temp)
                        rng = temp.find('\xa0')
                        temp = temp[0:rng]
                        print(temp)
                        temp = temp.replace(',', '')
                        temp = temp.replace('$', '')
                        temp = temp.replace('(', '-')
                        temp = temp.replace(')', '')
                        print(temp)
                        print("----------------")
                        self.wanted_data[w] = float(temp)
                        break
                    # Case 2b: " xxx yyy"
                    if text_file[i][len(w)].find(' ') != -1 and has_numb(text_file[i][len(w) + 1]) is True \
                            and text_file[i][len(w):].find('$') == -1 and text_file[i][len(w) + 1:].find(' ') != -1:
                        temp = text_file[i]
                        print("----------------")
                        print("CASE 2b")
                        print(temp)
                        rng = temp.find('\xa0')
                        temp = temp[rng + 1:]
                        print(temp)
                        rng = temp.find('\xa0')
                        temp = temp[0:rng]
                        print(temp)
                        temp = temp.replace(',', '')
                        temp = temp.replace('$', '')
                        temp = temp.replace('(', '-')
                        temp = temp.replace(')', '')
                        print(temp)
                        print("----------------")
                        self.wanted_data[w] = float(temp)
                        break
                # Case 3: numbers only, no indentation in the middle
                if text_file[i][len(w) + 1:].find(' ') == -1:
                    # Case 3: "xxxyyy" and " xxxyyy"
                    if (has_numb(text_file[i][len(w)]) is True or has_numb(text_file[i][len(w) + 1]) is True) \
                            and text_file[i][len(w):].find('$') == -1:
                        temp = text_file[i]
                        print("----------------")
                        print(temp)
                        temp = temp.replace(w, '')
                        print(temp)
                        # Case 3a: "(xxx)yyy " or (xxx)(yyy)
                        if text_file[i][len(w)].find('(') != -1 or text_file[i][len(w) + 1].find('(') != -1:
                            print("CASE 3a")
                            neg = text_file[i][len(w):].find(')')
                            temp = temp[:neg]
                            print(temp)
                            temp = temp.replace('(', '-')
                            temp = temp.replace(')', '')
                            temp = temp.replace(',', '')
                            print(temp)
                            print("----------------")
                            self.wanted_data[w] = float(temp)
                            break
                        # Case 3b: "xxx(yyy)
                        if text_file[i][len(w) + 2:].find('(') != -1:
                            print("CASE 3b")
                            neg = text_file[i][len(w):].find('(')
                            temp = temp[:neg]
                            print(temp)
                            temp = temp.replace('(', '')
                            temp = temp.replace(')', '')
                            temp = temp.replace(',', '')
                            print(temp)
                            print("----------------")
                            self.wanted_data[w] = float(temp)
                            break
                        # Case 3c: all other generic cases
                        else:
                            comma = temp.find(',')
                            # case 3c(i): if comma does exist
                            if comma != -1 and comma - len(w) < 4:
                                print("CASE 3c(i)")
                                while comma <= len(temp):
                                    if has_numb(temp[comma + 4]) is True:
                                        temp = temp[:comma + 4]
                                        temp = temp.replace(',', '')
                                        print(temp)
                                        print("----------------")
                                        self.wanted_data[w] = float(temp)
                                        break
                                    else:
                                        comma = comma + 4
                                        continue
                            # Case 3c(ii): no comma
                            else:
                                print("CASE 3c(ii)")
                                temp = temp.replace(' ', '')
                                if len(temp) == 6:
                                    temp = temp[0:2]
                                    print(temp)
                                    print("----------------")
                                    self.wanted_data[w] = float(temp)
                                if len(temp) == 5:
                                    # hard to tell if xxyyy or xxxyy
                                    print("inconclusive")
                                    # Figure out a good way to deal with this
                                    temp = "Either", float(temp[0:1]), "or", float(temp[0:2])
                                    print(temp)
                                    print("----------------")
                                    self.wanted_data[w] = temp
                                if len(temp) == 4:
                                    # hard to tell if xxyy or xxxy or xyyy
                                    print("inconclusive")
                                    temp = float(temp[0]), "or", float(temp[0:1]), "or", float(temp[0:2])
                                    self.wanted_data[w] = temp
                                    print(temp)
                                    print("----------------")
                                if len(temp) == 3:
                                    # hard to tell if xyy or xxy
                                    print("inconclusive")
                                    temp = "Either", float(temp[0]), "or", float(temp[0:1])
                                    self.wanted_data[w] = temp
                                    print(temp)
                                    print("----------------")
                                if len(temp) == 2:
                                    temp = temp[0]
                                    print(temp)
                                    print("----------------")
                                    self.wanted_data[w] = float(temp)
                                break

    def make_csv(self, filename, loc, year): #UNFINISHED
        """
        :param filename: name of the file 'example.csv'
        :param loc: location of the file
        :param year: time of the data
        :return:
        """
        with open(filename, loc) as csvfile:
            fieldnames = ["Financial Data", "Year 1", "Year 2", "Year 3", "Year 4", "Year 5"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for i in self.wanted_data:
                writer.writerow({'Financial Data': i, 'Year 1': self.wanted_data[i]})
    # https://www.sec.gov/Archives/edgar/data/1156375/000115637517000045/cme-201733110q.htm
    # https://www.sec.gov/Archives/edgar/data/1571949/000157194917000006/ice201733110q.htm
    # https://www.sec.gov/Archives/edgar/data/21344/000002134417000019/a2017033110-q.htm
    # https://www.sec.gov/Archives/edgar/data/719739/000071973917000021/sivb-3312017x10q.htm
    # https://www.sec.gov/Archives/edgar/data/1050915/000119312517164407/d353659d10q.htm
    # https://www.sec.gov/Archives/edgar/data/1534701/000153470117000074/psx-2017331_10q.htm
    # https://www.sec.gov/Archives/edgar/data/1126328/000110465917029273/a17-7605_110q.htm
    # https://www.sec.gov/Archives/edgar/data/70858/000007085817000025/bac-331201710xq.htm
    # https://www.sec.gov/Archives/edgar/data/1594864/000159486417000022/juno-03312017x10q.htm

s = EquityData("SIVB", '10-Q', 10)
pfg = s.historical_data('google', '2015-01-01')
# pfg.to_csv('C:/Users/kevin/Desktop/Financial data/pfg_data.csv')
# print(pfg)


# create_csv(pfg, "pfg.csv")
s.insert_into_dict("Cash and cash equivalents", s._text_list[1])
for e in s._text_list[1]:
    print(e)
print(s.load_data())