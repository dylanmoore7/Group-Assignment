"""
Dylan Moore 01/05/2022

This program opens a file from within the same directory as itself and reads each line to check it contains
valid data. The program takes the dates and volumes from each valid file line and appends them to two separate
lists (one inside the other). These lists are added to another list which is then divided into two lists
(february and march). These three lists of lists (March & February, March, February) are then processed by
the different functions and sorted by their different values (eg: day, volume, etc.) to
obtain the necessary values.
"""

import os.path  # only used to check if file exist in directory

# This function takes a list of lists, the second value for each inner list (trade volume)
#   is added to the total_volume variable.
# The items_counted variable is used for calculating the average later.
def total_trade_volume(list_argument):
    items_counted = 0
    total_volume = 0
    for item in list_argument:
        items_counted += 1
        total_volume += item[1]
    return total_volume, items_counted

# This function takes a list and sends it to the total_trade_volume function to get total_volume and items_counted.
# It then uses these values to calculate and return the average trade volume.
def average_trade_volume(list_argument):
    total_volume, items_counted = total_trade_volume(list_argument)
    average = total_volume / items_counted
    return average

# This function takes two lists and sends each one to the total_trade_volume function to get the total volume of each.
# To the total_volumes_list, it appends a list containing two values, [total_volumes_feb, "February"].
# To the total_volumes_list, it appends another list containing two values, [total_volumes_Mar, "March"].
# The list now looks like this [[total_volumes_feb, "February"], [total_volumes_mar, "March"]].
# This list is now sorted in reverse order by the volume values (the list with the highest value is now first).
# The month string inside that first list is returned.
def highest_volume_month(february_list, march_list):
    total_volumes_list = []
    total_volumes_feb, _ = total_trade_volume(february_list)
    total_volumes_list.append([total_volumes_feb, "February"])
    total_volumes_mar, _ = total_trade_volume(march_list)
    total_volumes_list.append([total_volumes_mar, "March"])
    total_volumes_list.sort(key=lambda volume: volume[0], reverse=True)
    # print(total_volume_list)
    return total_volumes_list[0][1]

# This function takes a list of lists and iterates through it, appending lists where the value (2) indicates  February
#   to a new list called february_list and lists where the value (3) indicates March to a new list called march_list.
# These lists are then returned.
def divide_list_into_months(every_line_list):
    february_list = []  # initialise list to hold only info from February.
    march_list = []  # initialise list to hold only info from March.
    for item in every_line_list:
        if item[0][1] == 2:
            february_list.append(item)
        elif item[0][1] == 3:
            march_list.append(item)
    return february_list, march_list

# Function takes a file and separates the date and volume on each line into two separate lists, one inside the other.
# Each valid line is split into two lists [[<day>,<month>,year>], <volume>] and then added to every_line_list
# If a line does not contain valid data the line is not appended to the list and an error message is shown.
def read_file(apple_file):
    every_line_list = []
    loop1_counter = 1  # used to keep track of what file line is being read so ERROR message can tell us

    for line in apple_file:
        is_valid_line = True  # to ensure it is never already false on a new line
        line = line.rstrip("\n")  # strips newline from each line
        one_line_list = line.split(',')  # splits the file line into a list (one_line_list) values separated at each ','
        one_line_list[0] = one_line_list[0].split('/')  # splits first item in list at each '/' to create inner list

        try:
            one_line_list[1] = int(one_line_list[1])  # tries to convert volume string to int
            loop2_counter = 0  # counter used in for loop below to iterate through the inner list

            for item in one_line_list[0]:  # for each item in the inner list, eg: [<day>, <date>, <year>]

                try:
                    one_line_list[0][loop2_counter] = int(item.lstrip('0'))  # try strip leading '0', convert to int
                    loop2_counter += 1  # add 1 to loop_counter if the above line succeeded

                except(Exception,):
                    print("\nERROR 2: file line ", loop1_counter, ' skipped, ', one_line_list, ' is invalid data', sep="")
                    is_valid_line = False  # if converting date to integer doesn't work, set is_valid_line to False
                    break  # if any of the values in this inner date list are invalid, break the loop

            if is_valid_line:
                # if still no errors, send to error check function (if statement to avoid sending already found error)
                is_valid_line = final_error_check(one_line_list)  # False if invalid, True if valid
                if is_valid_line:  # if still no errors after the error function
                    every_line_list.append(one_line_list)  # append this lines list to every_line_list
            else:
                is_valid_line = True  # If an error was found in inner for loop, now reset this variable to True.
                # Outer loop will now start again and move onto next file line.

        except(Exception,):
            # if the first test of converting volume to integer doesn't work, print error
            print("\nERROR 1: file line ", loop1_counter, ' skipped, ', one_line_list, ' is invalid data', sep="")
            # No need to set is_valid_line to False (this would

        loop1_counter += 1  # used to keep track of what file line is being read so ERROR message can tell us

    return every_line_list  # returns the complete list of lists

# This function takes march_list and february_list and sorts them by volume in forward and reverse
#   order so that the first list in the list contains either the highest or lowest volume (with corresponding date).
# Data is printed with thousands separator coma.
# total_trade_volume, average_trade_volume and highest_volume_month functions are called to obtain necessary values.
def sort_format_print(february_list, march_list, every_line_list):

    february_list.sort(key=lambda volume: volume[1], reverse=True)  # max trade vol in feb
    print("\n", february_list[0][0][0], "/", february_list[0][0][1], "/", february_list[0][0][2],
          " has the maximum trade volume of ", f'{february_list[0][1]:,d}', " in February.", sep="")

    february_list.sort(key=lambda volume: volume[1])  # min trade vol in feb
    print(february_list[0][0][0], "/", february_list[0][0][1], "/", february_list[0][0][2],
          " has the minimum trade volume of ", f'{february_list[0][1]:,d}', " in February.", sep="")

    march_list.sort(key=lambda volume: volume[1], reverse=True)  # max trade vol in mar
    print(march_list[0][0][0], "/", march_list[0][0][1], "/", march_list[0][0][2],
          " has the maximum trade volume of ", f'{march_list[0][1]:,d}', " in March.", sep="")

    march_list.sort(key=lambda volume: volume[1])  # min trade vol in mar
    print(march_list[0][0][0], "/", march_list[0][0][1], "/", march_list[0][0][2],
          " has the minimum trade volume of ", f'{march_list[0][1]:,d}', " in March.", sep="")

    total_volume, _ = total_trade_volume(every_line_list)
    print("\nThe whole trade volume of these two months is ", f'{total_volume:,d}')

    average_volume_feb = average_trade_volume(february_list)
    print("\nThe average trade volume of February is ", f'{round(average_volume_feb):,d}')

    average_volume_mar = average_trade_volume(march_list)
    print("The average trade volume of March is ", f'{round(average_volume_mar):,d}')

    month = highest_volume_month(february_list, march_list)
    print("\nAAPL has higher trading volume in", month)

# This function is called by read_file function to check for multiple errors / invalid data. True or False returned.
def final_error_check(one_line_list):
    is_valid_line = True
    if len(one_line_list) != 2:
        is_valid_line = False
    if len(one_line_list[0]) != 3:
        is_valid_line = False
    if 0 <= one_line_list[0][0] >= 32:
        is_valid_line = False
    if 0 <= one_line_list[0][1] >= 13:
        is_valid_line = False
    if 1989 <= one_line_list[0][2] >= 2089:
        is_valid_line = False
    return is_valid_line


def main():

    if os.path.exists("AAPL.txt"):  # Check if file exists in directory.
        apple_file = open("AAPL.txt", "r")  # Open the file.

        every_line_list = read_file(apple_file)  # Call every_line_list function.

        apple_file.close()  # Close file.

        february_list, march_list = divide_list_into_months(every_line_list)  # Call divide_list_into_months function.

        if len(february_list) < 1 or len(march_list) < 1:  # If either list has less than 1 item, print error.
            print("\nERROR 4: insufficient data to calculate")
        else:
            sort_format_print(february_list, march_list, every_line_list)  # Otherwise call sort_format_print function.

    else:
        print("\nERROR 0: missing file APPL.txt")  # If file doesn't exist print error.


main()  # Calls main function
