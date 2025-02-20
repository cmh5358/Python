'''
Title: National Flood Hazard Layer (NFHL) Download States
Author: Caitlin Hartig
Date: November 2024

This script is a web crawler that downloads data specifically from the NFHL website that are packaged in separate zip folders for each state / territory. The program then saves each zip folder into a designated folder pathway and then zips the final folder.

Libraries Utilized: selenium, urllib, shutil, datetime, os
'''

from selenium import webdriver
from selenium.webdriver.support.ui import Select
from urllib.request import urlretrieve
import shutil, datetime, os

##'''
##    Purpose - download_pdfs(url, lst_failed, folder_name, count) is a web crawler that downloads data in zip folders specifically from the NFHL website for each state / territory and saves them into a designated folder pathway (folder_name).
##    Inputs -url: a website url specifically for the NFHL website, to download data for each state / territory. Ex) r'https://hazards.fema.gov/femaportal/NFHL/searchResulthttps:/hazards.fema.gov/femaportal/NFHL/searchResult'.
##                This url should not be changed unless NFHL changes their website link.
##           -lst_failed: an empty list that will hold the indexes of failed states / territories to attempt to run a second time, in case the failure was due to temporary network issues
##           -folder_name: a folder pathway. Ex) r'C:\Users\CaitlinHartig\Documents\NFHL\Data'
##           -count: this counter must start at 0 and drives the program to re-run lst_failed
##    Outputs - None
##'''
def download_pdfs(url, lst_failed, folder_name, count):
  try: # Attempts to connect to the Chrome browser
      driver = webdriver.Chrome()
  except:
      print('Error! Unable to connect to browser.\n')
      quit()
  else:
      try: # Attempts to connect to the specified url
          driver.get(url)
      except:
          print('Error! Unable to get URL. Check URL.')
          print('\turl: ', url, '\n')
          quit()
      else:
          try: # Attempts to obtain a list of states / territories in the drop-down menu
              lst_states = Select(driver.find_element(webdriver.common.by.By.NAME, 'state'))
              last_index =  len(lst_states.options) # Finds the total number of options in the list of states / territories in the drop-down menu
          except:
              print('Error! Unable to obtain full list of states / territories. Check URL, site may be under maintenance.')
              print('\turl: ', url, '\n')
              quit()
          else:
              if len(lst_failed) != 0:
                  last_index = len(lst_failed) # Finds the total number of options in the list of failed states / territories
                  lst_failed_copy = lst_failed
                  lst_failed = []
                  
              for index in range(1, last_index):
                  
                  if len(lst_failed) != 0:
                      index = lst_failed_copy[index - 1]
                  
                  try: # Attempts to connect to the Chrome browser
                      driver = webdriver.Chrome()
                  except:
                      print('Error! Unable to connect to browser.\n')
                      lst_failed.append(index)
                  else:
                      try: # Attempts to connect to the specified url
                        driver.get(url)
                      except:
                        print('Error! Unable to get URL.')
                        lst_failed.append(index) # Index appended to lst_failed to try running a second time in case the failure was due to a temporary network issue
                      else:
                        try: # Attempts to select the state by index
                            lst_states = Select(driver.find_element(webdriver.common.by.By.NAME, 'state'))
                            lst_states.select_by_index(index)
                        except:
                            print('Error! Unable to select state / territory.\n')
                            lst_failed.append(index) # Index appended to lst_failed to try running a second time in case the failure was due to a temporary network issue
                        else:
                            try: # Attempts to click the button to obtain more information for the state / territory
                                get_state_button = driver.find_element(webdriver.common.by.By.NAME, 'submitState')
                                get_state_button.click()
                            except:
                                print('Error! Unable to obtain info for selected state / territory.\n')
                                lst_failed.append(index) # Index appended to lst_failed to try running a second time in case the failure was due to a temporary network issue
                            else:
                                try: # Attempts to find the href value containing the unique download link for this state / territory
                                    element = driver.find_element(webdriver.common.by.By.XPATH, r'//td[last()]/center/a')
                                    href_value = element.get_attribute("href")
                                except:
                                    print('Error! Unable to obtain href value. Webpage may be under maintenance.\n')
                                    lst_failed.append(index) # Index appended to lst_failed to try running a second time in case the failure was due to a temporary network issue
                                else:
                                    try: # Attempts to find the unique download link to download the zip folder for this state / territory
                                        file_index = href_value.rfind('=')
                                        file = href_value[file_index + 1:]
                                    except:
                                        print('Error! Unable to obtain file name.')
                                        print('\thref value: ', href_value, '\n')
                                    else:
                                        if not os.path.exists(folder_name): # Makes a new directory for the specified folder if one does not already exist
                                            os.makedirs(folder_name)
                                        
                                        filename = r'{0}\{1}'.format(folder_name, file) # Saves the file in the specified folder
                                        print(filename, '\n')

                                        try:
                                          urlretrieve(href_value, filename)
                                        except:
                                          print('Error! Unable to download zip folder.')
                                          lst_failed.append(index) # Index appended to lst_failed to try running a second time in case the failure was due to a temporary network issue
                                        finally:
                                          driver.quit()

              if len(lst_failed) != 0:
                  count += 1
                  if count < 2: # Rerun the program a second time in the event that any indexes failed due to temporary network issues
                      download_pdfs(url, lst_failed, folder_name, count)
                  else:
                      driver.quit()
                      print('All NFHL data downloaded, except:\n')
                      for failed_index in lst_failed:
                          print('\tFailed index: ', failed_index, '\n') # Prints the list of failed states / territories
                      print('Please manually download the above failed indexes from \n\t{0}\n.'.format(url))
                      print('Then, manually zip the folder located here:\n\t', folder_name)
                      quit()
              else:
                  driver.quit()
                  print('All NFHL data downloaded.\n')
                    
##'''
##    Purpose - zip_folder(folder_name) takes a pathway to a folder that needs to be zipped.
##    Inputs - A folder pathway folder_name. Ex) r'C:\Users\CaitlinHartig\Documents\NFHL\Data'
##    Outputs - None
##'''
def zip_folder(folder_name):
    if os.path.isdir(folder_name): # Creates a .zip folder name for the specified folder
        zip_name = folder_name + '.zip'

        if os.path.exists(zip_name): # If the .zip folder already exists, it is removed
            os.remove(zip_name)
        
        shutil.make_archive(folder_name, 'zip', folder_name) # Specified folder is zipped

        print('Folder zipped.\n')
    else:
        print('Error! Folder directory does not exist.\n')
    
if __name__ == '__main__':
    print("Job starting!", datetime.datetime.now(), "\n")
    
    url = r'https://hazards.fema.gov/femaportal/NFHL/searchResulthttps:/hazards.fema.gov/femaportal/NFHL/searchResult' # Do not update unless the url has changed. This url should be specifically the NFHL website
    folder = r'C:\Users\CaitlinHartig\Documents\NFHL\Data' # Update me!

    lst_failed = [] # This list will hold the indexes of failed states / territories to attempt to run a second time, in case the failure was due to temporary network issues
    count = 0 # This counter must start at 0 and drives the program to re-run lst_failed
    
    download_pdfs(url, lst_failed, folder, count)

    zip_folder(folder)

    print("\nJob ending!", datetime.datetime.now(), "\n")
