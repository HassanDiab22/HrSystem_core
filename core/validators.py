from django.core.exceptions import ValidationError

def validate_timesheet_dates(start_date, end_date,timesheets):
    if  start_date > end_date:
            raise ValidationError('Start date cannot be greater than end date.')
    if  start_date == end_date:
            raise ValidationError('End date cannot be same date as the start date.')
    for timesheet in timesheets:
           if start_date >= timesheet.startdate and end_date <=  timesheet.enddate :
               raise ValidationError('Timesheet with these dates already exist')   