#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""

author: Roey Bretschneider

"""

import wx
import wx.adv as advance_gui
import datetime
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.common.action_chains import ActionChains
import  threading

REQUESTS_LIST = []

class send_date():
    def __init__(self):
        pass

    def search_contact(self,name ):
        # press on the look window
        # look_for_xpath = '//label[@data-icon = "_2MSJr"]'
        look_for_xpath = '//span[@data-icon= "search"]'
        # look_for_xpath='//div[contains(text(), "{0}") and @class="inner"]'.format(text)
        look_for_elem = self.driver.find_element_by_xpath(look_for_xpath)
        look_for_elem.click()
        # search the window
        # look_for2_xpath = '//div[@class = "_3u328 copyable-text selectable-text"]'
        look_for2_xpath = '//div[@contenteditable= "true"][@data-tab="3"]'
        look_for_elem2 = self.driver.find_element_by_xpath(look_for2_xpath)
        look_for_elem2.clear()
        look_for_elem2.send_keys(name)

    def press_contact_after_search(self,name):
        # x_arg = '//div[@class="KgevS"]//span[contains(@class,"matched-text")]'
        x_arg_contact = '//span/span[@title= "{0}"]'.format(name)#FIXME there is difference between group and simgal contact
        #group contains only 2 spans (not like person)
        try:
            time.sleep(0.5)
            group_title = self.driver.find_element_by_xpath(x_arg_contact)
            #FIXME add timeout
        except:
            try:
                x_arg_group='//div//descendant::span[@title= "{0}"]'.format(name)
                group_title = self.driver.find_element_by_xpath(x_arg_group)
            except:
                raise NameError('no contact')
        group_title.click()
        print("pressed on contact")

    def send_button(self,massage):
        # press on input box and send text
        # inp_xpath = '//div[@class="_3u328 copyable-text selectable-text"][@spellcheck="true"]'
        inp_xpath = '//div[@contenteditable= "true"][@data-tab="6"]'
        #inp_xpath = '//div[@contenteditable= "true"]'
        input_box = self.wait.until(EC.presence_of_element_located((
            By.XPATH, inp_xpath)))

        for i in range(1):
            input_box.send_keys(massage + Keys.ENTER)  #
            time.sleep(1)
        print("sanded the massage")

    def send_massage(self,name, massage,driver):
        """
        function for sending whatsapp massage
        :param name: contact name
        :param massage: the data
        :param driver: driver
        :return:
        """
        self.driver=driver
        self.wait= WebDriverWait(self.driver, 600)

        self.search_contact(name)
        self.press_contact_after_search(name)
        self.send_button(massage)


##################################################
class Request():
    def __init__(self, contact, date, massage,index):
        self.contact = contact #str
        self.date = date    #datetime.datetime
        self.massage = massage #str
        self.index = index #int
    def __str__(self):
        return 'date {0} contact = {1} massage = {2} index = {3}'.format(self.date,self.contact,self.massage,self.index)

#######################################################

class Example(wx.Frame):

    def __init__(self, parent, title):
        super(Example, self).__init__(parent, title=title)
        #ewsponsabole to enter the right place on list
        self.index = 0
        #responsebole to keep trace after requests and delete them

        self.InitUI()  # create things like buttons and stuff (everything inside the up in frontend)
        self.Centre()  # put app in center

    def InitUI(self):
        """
        create app
        :return:
        """
        panel = wx.Panel(self)

        font = wx.SystemSettings.GetFont(wx.SYS_SYSTEM_FONT)

        font.SetPointSize(9)
        # add contact box
        # vbox
        vbox = wx.BoxSizer(wx.VERTICAL)
        # create horizon1
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        # add first thing
        st1 = wx.StaticText(panel, label='Contact:')
        st1.SetFont(font)
        hbox1.Add(st1, flag=wx.RIGHT, border=20)
        # add first second thing
        self.contact = wx.TextCtrl(panel)
        hbox1.Add(self.contact, proportion=1)
        # add horizon1
        vbox.Add(hbox1, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)
        # add space
        vbox.Add((-1, 4))
        ########
        # create massage box
        # create horizon 2
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        # add massage
        st2 = wx.StaticText(panel, label='Massage:')
        st2.SetFont(font)
        hbox2.Add(st2, flag=wx.RIGHT, border=20)
        # add second thing
        self.massage = wx.TextCtrl(panel, style=wx.TE_MULTILINE)
        hbox2.Add(self.massage, proportion=1)

        # add horizon 2
        vbox.Add(hbox2, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)
        ######
        # DATE LINE
        vbox.Add((-1, 10))
        hbox3 = wx.BoxSizer(wx.HORIZONTAL)

        st3 = wx.StaticText(panel, label='Date:')
        st3.SetFont(font)
        hbox3.Add(st3, flag=wx.RIGHT, border=20)

        self.dpc1 = wx.adv.DatePickerCtrl(panel, wx.ID_ANY, wx.DefaultDateTime, style=advance_gui.DP_DROPDOWN)
        hbox3.Add(self.dpc1, flag=wx.RIGHT | wx.LEFT, border=20)

        self.tpc1 = wx.adv.TimePickerCtrl(panel, wx.ID_ANY, wx.DefaultDateTime)
        hbox3.Add(self.tpc1, flag=wx.Left, border=100)
        vbox.Add(hbox3, flag=wx.EXPAND | wx.LEFT | wx.TOP | wx.RIGHT, border=10)

        vbox.Add((-1, 25))
        ########
        # add table of time,contact and massage
        hbox4 = wx.BoxSizer(wx.HORIZONTAL)
        self.list_ctrl = wx.ListCtrl(panel, wx.ID_ANY, style=wx.LC_REPORT
                                                             | wx.BORDER_SUNKEN)
        self.list_ctrl.InsertColumn(0, 'time')
        self.list_ctrl.InsertColumn(1, 'contact')
        self.list_ctrl.InsertColumn(2, 'massage', width=125)
        hbox4.Add(self.list_ctrl, proportion=1)
        vbox.Add(hbox4, flag=wx.EXPAND | wx.LEFT | wx.TOP | wx.RIGHT, border=10)

        #####
        # add 2 buttons
        hbox5 = wx.BoxSizer(wx.HORIZONTAL)
        btn1 = wx.Button(panel, label='Add', size=(70, 30))
        btn1.Bind(wx.EVT_BUTTON, self.add_line)
        hbox5.Add(btn1)
        btn2 = wx.Button(panel, label='Delete', size=(70, 30))
        btn2.Bind(wx.EVT_BUTTON, self.remove_line)
        hbox5.Add(btn2, flag=wx.LEFT | wx.BOTTOM, border=5)
        vbox.Add(hbox5, flag=wx.ALIGN_RIGHT | wx.RIGHT, border=10)

        panel.SetSizer(vbox)
        vbox.Fit(self)

    def add_line(self, event):
        """
        add line in the gui and add line to the list of massage to send
        :param event:
        :return:
        """
        print(self.list_ctrl.GetFirstSelected())
        # enter date
        time_chosen = self.dpc1.GetValue()
        in_day_time = self.tpc1.GetValue()
        #FIXME magic number 1, there because of a bug in the libary
        date = datetime.datetime(year=time_chosen.GetYear(), month=time_chosen.GetMonth()+1, day=time_chosen.GetDay(),
                                 hour=in_day_time.GetHour(), minute=in_day_time.GetMinute())
        #line = "time %s" % date
        line = str(date)
        self.list_ctrl.InsertStringItem(self.index, line)
        # enter contact name
        contact_name = self.contact.GetLineText(0)
        print(contact_name)
        # enter massage
        massage = self.massage.GetValue()
        print(massage)
        self.list_ctrl.SetStringItem(self.index, 1, contact_name)
        self.list_ctrl.SetStringItem(self.index, 2, massage)

        # add request to REQUEST_LIST change tume chosen

        print(date)
        REQUESTS_LIST.append(Request(massage=massage, date=date, contact=contact_name,index= self.index))
        print("index = " + str(self.index))
        self.index += 1



    def remove_line(self, e):
        """
        allowing remove a massage was already registered
        :param e:
        :return:
        """
        #print(type(self.dpc1.GetValue()))
        inedx = self.list_ctrl.GetFirstSelected()
        if inedx != -1:
            self.index -= 1
            self.list_ctrl.DeleteItem(inedx)
            for i in REQUESTS_LIST:
                #print(i)
                if i.index==inedx:
                    REQUESTS_LIST.remove(i)
            self.update_after_remove(inedx)
        for i in REQUESTS_LIST:
            print(i)
    # get index of pressed line and arrange indexes is list to be following (1,2,3,4,5)
    def update_after_remove(self,index):
        for i in REQUESTS_LIST:
            if i.index>index:
                i.index-=1

#######################################


def compare_times(now,date1):
    """
    check if the times are equal to each other until the minutes (include minutes)
    :param now: fist date compared
    :param date1: second date compared
    :return:
    """
    print("enter compare date")
    try:
        if now.year==date1.year and now.month==date1.month and now.day==date1.day and now.hour==date1.hour and now.minute == date1.minute:
            print("true")
            return True
        else:
            return False
    except Exception as err:
        print (err)

def whatsapp_thread():
    """
    thread in charge of sending the massages
    :return:
    """
    driver = webdriver.Chrome()
    driver.get("https://web.whatsapp.com/")
    wait = WebDriverWait(driver, 600)

    while (True):

        now = datetime.datetime.now()
        print("hour= " + str(now.hour) + "  min = " + str(now.minute))

        for i in REQUESTS_LIST:
            if compare_times(now,i.date):
                d= send_date()
                try:
                    d.send_massage(i.contact,i.massage,driver)
                except  NameError as err:
                    if str(err) == 'no contact':
                        global ex
                        ex.contact.SetValue("")
                        ex.contact.write("invalid contact = '{0}'".format(i.contact))

                        print("invalid contact name")

        time.sleep(60)
        # name = input("enter name of contact")
        # massage= input("enter the massage")
        # send_massage(name,massage)
        # break


def main():
    """
    create 2 main threads
    gui thread
    whatsapp thread
    :return:
    """
    global ex
    app = wx.App()
    ex = Example(None, title='Go To Class')
    ex.Show()
    t=threading.Thread(target=whatsapp_thread)
    t.start()
    app.MainLoop()

    #now = datetime.datetime.now()
    #print(str(now))
    #print(now.day)


if __name__ == '__main__':
    main()
