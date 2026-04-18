import logging

def process_data(data):
    try:
        value = int(data.get("value", 0))

        if value > 10:
            return "High"
        else:
            return "Low"

    except Exception as e:
        logging.error(f"Error in processing: {str(e)}")
        raise