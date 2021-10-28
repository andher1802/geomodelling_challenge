from utils import argument_handler
import datetime

def set_arguments_values():
    """
    This function prepares the set of input parameters for the collection of images
    It uses the argument_handler class to read the input parameters from the terminal
    each parameters consists of type (String, Date, Integer), help message, and default_value.
    For this task we added four parameters:
    - start_date: Start date for search images in the data catalog
    - End date: End date for searching images in the data catalog
    - Input_geometry: Path to the geojson file for the search of data catalog
    - Folder: Path to folder where the results will be stored
    """
    arg_handler = argument_handler.Arguments_handler()
    arg_input_geometry = argument_handler.Argument("input_geometry")
    arg_input_geometry.set_argument_type("String")
    arg_input_geometry.set_argument_help_message("Path to the input geometry (.geojson) to intersect sentinel data (relative to the parent folder)")
    arg_input_geometry.set_argument_default_value("./input_geometries/doberitz_multipolygon.geojson")
    arg_handler.add_input_argument(arg_input_geometry)
    arg_folder = argument_handler.Argument("folder")
    arg_folder.set_argument_type("String")
    arg_folder.set_argument_help_message("Folder path to write the resulting data (relative to the parent folder)")
    arg_folder.set_argument_default_value("./sentinel_data")
    arg_handler.add_input_argument(arg_folder)
    arg_start_date = argument_handler.Argument("start_date")
    arg_start_date.set_argument_type("Date")
    arg_start_date.set_argument_help_message("Start date to process format DD-MM-YYYY (hyphen sep)")
    default_end_date = datetime.date.today()
    default_start_date = (default_end_date - datetime.timedelta(days=60)).strftime('%d-%m-%Y')
    arg_start_date.set_argument_default_value(default_start_date)
    arg_handler.add_input_argument(arg_start_date)
    arg_end_date = argument_handler.Argument("end_date")
    arg_end_date.set_argument_type("Date")
    arg_end_date.set_argument_help_message("End date to process format DD-MM-YYYY (hyphen sep)")
    arg_end_date.set_argument_default_value(default_end_date.strftime('%d-%m-%Y'))
    arg_handler.add_input_argument(arg_end_date)
    return arg_handler

def args_validation(args):
    """
    This function validates that the start and end dates parameters
    have the appropriate format, also includes a validation for Integer types
    and Integer_no_zero types in case they are required by the user.
    input: args (the input arguments set by the user)
    """
    input_parameters_raw = args.get_input_arguments()
    input_parameters_checked = {}
    for arg in args.arguments:
        if arg.argument_type_name == "Date":
            try:
                if type(input_parameters_raw[arg.argument_name]) is datetime.datetime:
                    input_parameters_checked[arg.argument_name] = input_parameters_raw[arg.argument_name]
                elif type(input_parameters_raw[arg.argument_name]) is str:
                    temp_argument_type_date = datetime.datetime.strptime(input_parameters_raw[arg.argument_name], '%d-%m-%Y')
                    input_parameters_checked[arg.argument_name] = temp_argument_type_date
            except:
                print("wrong date format {0} date should match dd-mm-yyyy. {0} ommited".format(arg.argument_name))
        elif arg.argument_type_name == "Integer" or arg.argument_type_name == "Integer_no_zero":
            if not type(input_parameters_raw[arg.argument_name]) is int:
                raise TypeError("Only integers are allowed") 
        elif arg.argument_type_name == "Integer_no_zero" and input_parameters_raw[arg.argument_name] < 0:
            raise Exception("Sorry, no numbers below zero")
        else:
            input_parameters_checked[arg.argument_name] = input_parameters_raw[arg.argument_name]
    return input_parameters_checked
      
def set_arguments_pipeline():
    """
    This function validates that dates are correct (end date after start date)
    and set the input parameters to a validated dictionary which can be used 
    in the subsequent processes.
    """
    input_parameters_checked = args_validation(set_arguments_values())
    days_timedelta = input_parameters_checked['end_date'] - input_parameters_checked['start_date']
    days_int = days_timedelta.days
    if days_int < 0:
        raise Exception('Start date should be set before end date')
    download_end = input_parameters_checked['start_date'] + datetime.timedelta(days_int)
    download_start_date = input_parameters_checked['start_date'].strftime('%Y-%m-%d')
    download_end_date = download_end.strftime('%Y-%m-%d')
    user_input_parameters = {
        'start_date': download_start_date,
        'end_date': download_end_date,
        'folder': input_parameters_checked['folder'],
        'input_geometry': input_parameters_checked['input_geometry']
    }
    return user_input_parameters