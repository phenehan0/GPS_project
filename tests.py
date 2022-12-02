from gps_functions import calculate_time_difference

"""
TEST CASES
1.) 
=============================================================================================
Pass the dimensions of the CSV to a function. 
Define a nested loop that iterates over the columns (at the upper level) and the rows (at the lower level).
Initialize one counter before entering into the outer loop, and a second counter
after entering into the outer loop and before entering into the inner loop (such that the
second counter will be re-initialized every time that the outer loop completes an iteration). 

The second counter will keep track of the number of rows for each column. The first counter will keep track of the number of rows.
After breaking out of the inner loop, compare the value of the row counter to the desired number of rows. 
If the values are not equal, the test case will fail. 
Similarly, compare the value of the column counter to the expected number of columns after exiting the
outer loop. If these values are not equal, then the test case will fail.
=============================================================================================


2.)
=============================================================================================

Test the function that calculates the distance between two geographic locations
by cross-referencing the output with a known/expected value for the distance (these can be sourced from the
internet, among other places). 
For example, Logan International Airport in Boston, MA is located at 
~87 West and ~42 North. O'Hare International Airport in Chicago, IL is located
at ~42 North and ~87 West. 
The shortest air distance from Boston to Chicago is ~1365 km. 

If the output if approximately equal to the expected result, then the test should be considered a success; otherwise, the test should be considered a failure.
=============================================================================================


3.) 
=============================================================================================
Test the conversion of string date/times to timestamps, and the
calculation of differences between timestamps. For the sake of time, the formatting convention and time zone of the 
GPS dataset CSV are assumed (YYYY-MM-DD HH:MM:SS +0000) (implemented below).

=============================================================================================

"""

def test_time_delta_calculation(start_time,end_time, target_days, target_hours, target_mins, target_sec):
    result = True
    if start_time[-6:] != " +0000":
        start_time += " +0000"
    if end_time[-6:] != " +0000":
        end_time += " +0000"
    print("Time elapsed from "+start_time+ " to: "+end_time+":")        
    delta = calculate_time_difference(start_time, end_time)
    days = int(delta / 86400)
    if days != target_days:
        result = False
    days_rem = delta % 86400
    hours = int(days_rem / 3600)
    if hours != target_hours:
        result = False
    hours_rem = int(days_rem % 3600)
    minutes = int(hours_rem / 60)
    if minutes != target_mins:
        result = False
    seconds = int(hours_rem % 60)
    if seconds != target_sec:
        result = False
        
    print(str(days)+" days "+str(hours)+" hours "+str(int(minutes)) + " minutes and "+ str(seconds)+ " seconds")
    return result


if __name__ == "__main__":
    # example test inputs
    test_time_delta_calculation("2018-03-13 21:16:42", "2018-03-13 21:23:09 +0000", 0, 0, 6, 27)
    test_time_delta_calculation("2018-03-13 06:53:17 +0000", "2018-04-04 11:34:28 +0000", 22, 4, 41, 11)
