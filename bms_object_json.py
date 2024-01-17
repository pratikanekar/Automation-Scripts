import pandas as pd
import json

def read_excel_and_create_json(filename):
    try:
        xls = pd.ExcelFile(filename)
        sheet_names = xls.sheet_names
        final_obj_json = {}
        for sheet_name in sheet_names:
            df = pd.read_excel(filename, sheet_name)
            # print(f"\nSheet Name: {sheet_name}\n")
            sheet_json = {}

            for column_name in df.columns:
                if column_name == 'Sr No' or column_name == 'Template Name':
                    continue  # Skip these columns

                zones_data = {}

                for index, row in df.iterrows():
                    template_name = row['Template Name']
                    if template_name == "object_name":
                        if str(row[column_name]).lower() == 'nan':
                            obj_name = ""
                        else:
                            obj_name = row[column_name]
                    elif template_name == "footer_query":
                        if str(row[column_name]).lower() == 'nan':
                            footer = ""
                        else:
                            footer = row[column_name].replace('\\n', ' \n').replace('\\"', '\"')
                    elif template_name == "object_unit":
                        if str(row[column_name]).lower() == 'nan':
                            unit = None
                        else:
                            unit = row[column_name]
                    elif template_name == "object_min_thresh":
                        if str(row[column_name]).lower() == 'nan':
                            min_thresh = None
                        else:
                            min_thresh = row[column_name]
                    elif template_name == "object_max_thresh":
                        if str(row[column_name]).lower() == 'nan':
                            max_thresh = None
                        else:
                            max_thresh = row[column_name]
                    elif template_name == "baseline":
                        if str(row[column_name]).lower() == 'nan':
                            base = None
                        else:
                            base = row[column_name]
                    elif template_name == "multiplier":
                        if str(row[column_name]).lower() == 'nan':
                            multi = None
                        else:
                            multi = row[column_name]
                    else:
                        column_value = row[column_name]

                        if template_name not in zones_data:
                            zones_data[template_name] = [column_value]
                            if str(column_value).lower() == 'nan' or column_value is None:
                                zones_data[template_name] = [""]
                        else:
                            zones_data[template_name].append(column_value)
                            if str(column_value).lower() == 'nan' or column_value is None:
                                zones_data[template_name] = [""]
                        if sheet_name == "MAIN_DASHBOARD":
                            sheet_json[column_name] = {
                                "object_name": obj_name,
                                "zones": zones_data,
                                "footer_query": footer,
                                "object_unit": unit,
                                "object_min_thresh": min_thresh,
                                "object_max_thresh": max_thresh,
                                "baseline": base,
                                "multiplier": multi
                            }
                        elif str(template_name).lower() == "nan":
                            sheet_json[column_name] = {
                                "object_name": obj_name,
                                "zones": [],
                                "footer_query": footer,
                                "object_unit": unit,
                                "object_min_thresh": min_thresh,
                                "object_max_thresh": max_thresh
                            }
                        else:
                            sheet_json[column_name] = {
                                "object_name": obj_name,
                                "zones": zones_data,
                                "footer_query": footer,
                                "object_unit": unit,
                                "object_min_thresh": min_thresh,
                                "object_max_thresh": max_thresh
                            }

                final_obj_json[sheet_name] = sheet_json
        with open('obj_mapping_test.json', 'w') as json_file:
            json.dump(final_obj_json, json_file, indent=2)

    except Exception as e:
        print(f"An error occurred: {e}")

# Update the file path accordingly
excel_file_path = 'Objects_json_mapping_zone.xlsx'
read_excel_and_create_json(excel_file_path)
