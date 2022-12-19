'''
Title: Joe's Automotive Services
Author: Caitlin Hartig
Date: 12/8/22

This GUI program uses check buttons to display the cost of routine maintenance services at Joe's Automotive:
    oil change, lube job, radiator flush, transmission flush, inspection, muffler replacement, and tire rotation.
When the "Calculate Total Price" button is clicked, the total cost of all services rendered is calculated.

Tools Utilized: tkinter, lists, functions
'''

import tkinter
import tkinter.messagebox

class MyGUI:
    '''
    This class creates the GUI.
    '''
    def __init__(self):
        '''
        This constructor creates 7 check buttons containing the cost of routine maintenance services at Joe's Automotive:
        oil change, lube job, radiator flush, transmission flush, inspection, muffler replacement, and tire rotation.
        It then calls the "do_something" function to add the prices of selected services to a list.
        When the "Calculate Total Price" button is clicked, the "calculate" function is called, which calculates the total price.
        '''
        self.main_window = tkinter.Tk()
        self.top_frame = tkinter.Frame()
        self.bottom_frame = tkinter.Frame()

        checkbox_var1 = tkinter.IntVar()
        checkbox_var2 = tkinter.IntVar()
        checkbox_var3 = tkinter.IntVar()
        checkbox_var4 = tkinter.IntVar()
        checkbox_var5 = tkinter.IntVar()
        checkbox_var6 = tkinter.IntVar()
        checkbox_var7 = tkinter.IntVar()

        # Check button 1
        self.check_button1 = tkinter.Checkbutton(self.top_frame, \
                                        text='Oil Change--$30.00', \
                                        command=self.do_something1, \
                                        variable=checkbox_var1, onvalue=1, offvalue=0)
        self.check_button1.pack()

        # Check button 2
        self.check_button2 = tkinter.Checkbutton(self.top_frame, \
                                        text='Lube Job--$20.00', \
                                        command=self.do_something2, \
                                        variable=checkbox_var2, onvalue=1, offvalue=0)
        self.check_button2.pack()

        # Check button 3                
        self.check_button3 = tkinter.Checkbutton(self.top_frame, \
                                        text='Radiator Flush--$40.00', \
                                        command=self.do_something3, \
                                        variable=checkbox_var3, onvalue=1, offvalue=0)
        self.check_button3.pack()

        # Check button 4                
        self.check_button4 = tkinter.Checkbutton(self.top_frame, \
                                        text='Transmission Flush--$100.00', \
                                        command=self.do_something4, \
                                        variable=checkbox_var4, onvalue=1, offvalue=0)
        self.check_button4.pack()
        
        # Check button 5        
        self.check_button5 = tkinter.Checkbutton(self.top_frame, \
                                        text='Inspection--$35.00', \
                                        command=self.do_something5, \
                                        variable=checkbox_var5, onvalue=1, offvalue=0)
        self.check_button5.pack()

        # Check button 6        
        self.check_button6 = tkinter.Checkbutton(self.top_frame, \
                                        text='Muffler Replacement--$200.00', \
                                        command=self.do_something6, \
                                        variable=checkbox_var6, onvalue=1, offvalue=0)
        self.check_button6.pack()

        # Check button 7        
        self.check_button7 = tkinter.Checkbutton(self.top_frame, \
                                        text='Tire Rotation--$20.00', \
                                        command=self.do_something7, \
                                        variable=checkbox_var7, onvalue=1, offvalue=0)
        self.check_button7.pack()
        
        # Calculate Total Price button
        self.calc_button = tkinter.Button(self.bottom_frame, \
                                        text='Calculate Total Price:', \
                                        command=self.calculate)
        self.calc_button.pack(side='left', pady=20)

        # This label shows the calculated total price after the above button is clicked
        self.value = tkinter.StringVar()
        self.total_label = tkinter.Label(self.bottom_frame,
                                         textvariable=self.value)
        self.total_label.pack(side='left', pady=20, padx=5)

        self.top_frame.pack()
        self.bottom_frame.pack()        

        tkinter.mainloop()

    global lst
    lst = [] # This empty list will hold the price values for all selected services
                
    def do_something1(self):
        '''
        This function appends the price value for the service to the list if checked (Button 1).
        '''
        value = 30.00
        lst.append(value)

    def do_something2(self):
        '''
        This function appends the price value for the service to the list if checked (Button 2).
        '''
        value = 20.00
        lst.append(value)

    def do_something3(self):
        '''
        This function appends the price value for the service to the list if checked (Button 3).
        '''
        value = 40.00
        lst.append(value)

    def do_something4(self):
        '''
        This function appends the price value for the service to the list if checked (Button 4).
        '''
        value = 100.00
        lst.append(value)

    def do_something5(self):
        '''
        This function appends the price value for the service to the list if checked (Button 5).
        '''
        value = 35.00
        lst.append(value)

    def do_something6(self):
        '''
        This function appends the price value for the service to the list if checked (Button 6).
        '''
        value = 200.00
        lst.append(value)

    def do_something7(self):
        '''
        This function appends the price value for the service to the list if checked (Button 7).
        '''
        value = 20.00
        lst.append(value)

    def calculate(self):
        '''
        This function calculates the total price of all services checked (rendered).
        '''
        total = sum(lst)
        print(total)
        self.value.set(total)

if __name__ == '__main__':
    my_gui = MyGUI()