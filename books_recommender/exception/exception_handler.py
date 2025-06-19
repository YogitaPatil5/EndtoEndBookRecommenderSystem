import os
import sys

class AppException(Exception):
    """
    AppException is customized exception class designed to capture refined details about exception
    such as python script file line number along with error message
    With custom exception one can easily spot source of error and provide quick fix.
    It takes two parameters:
    error_message: The error message to be displayed
    error_detail: The error detail to be displayed
    """
    
    def __init__(self, error_message: Exception, error_detail: sys):
        """
        This method is used to get the detailed error message
        It takes two parameters:
        error_message: The error message to be displayed
        error_detail: The error detail to be displayed
        It returns the detailed error message
        """
        super().__init__(error_message)
        self.error_message = AppException.error_message_detail(error_message, error_detail=error_detail)

    @staticmethod
    def error_message_detail(error_message: Exception, error_detail: sys):
        """
        This method is used to get the detailed error message
        It takes two parameters:
        error_message: The error message to be displayed
        error: The Exception object raised from module
        error_detail: The error detail to be displayed
        It returns the detailed error message
        """
        _,_,exc_tb = error_detail.exc_info()
        ## exctracting file name from where exception traceback is raised
        file_name = exc_tb.tb_frame.f_code.co_filename
        error_message = f"Error occurred in python script name [{file_name}] line number [{exc_tb.tb_lineno}] error message [{error_message}]"
        return error_message
    
    def __repr__(self):
        """
        formating object of AppException
        """

        return AppException.__name__.__str__()
    
    def __str__(self):
        """
        Formating how a object should be visible in print statement

        """
        
        return self.error_message
    

        line_number = exc_tb.tb_frame.f_lineno