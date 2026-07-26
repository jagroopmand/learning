class Employee:
   def __init__(self, name, start_date:int):
      self.name = "emp1"
      self.start_date = start_date
    

class Status:
   def __init__(self, status:str, overdue_days:int):
      self.status = status
      self.overdue_days = overdue_days


def check_status(employee: Employee, training_completion_date:int, training_window_days:int, compliance_check_date:int) -> Status:
        if employee.start_date > compliance_check_date:
           return Status("not required", 0)
        else:
            if training_completion_date is None:
                if employee.start_date + training_window_days > compliance_check_date:
                   return Status("pending", 0)
                else:
                    overdue_days = compliance_check_date - (employee.start_date + training_window_days)
                    return Status("overdue", overdue_days)
            else:
                return(Status("completed", 0))        


if __name__  == "__main__":
   status = check_status(Employee("emp1", 100), None, 10, 99)
   print("status:: ", status.status, status.overdue_days) # not required, 0

   status = check_status(Employee("emp1", 100), None, 10, 109)
   print("status:: ", status.status, status.overdue_days) # pending, 0

   status = check_status(Employee("emp1", 100), None, 10, 111)
   print("status:: ", status.status, status.overdue_days) # overdue, 1

   status = check_status(Employee("emp1", 100), 105, 10, 111)
   print("status:: ", status.status, status.overdue_days) # completed, 0

   status = check_status(Employee("emp1", 100), 105, 10, 106)
   print("status:: ", status.status, status.overdue_days) # completed, 0

   status = check_status(Employee("emp1", 100), 111, 10, 112)
   print("status:: ", status.status, status.overdue_days) # completed, 0