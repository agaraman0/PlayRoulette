
class StatusMessage:
    FAILED: str = "failed"
    SUCCESS: str = "success"


class APIResponseClass:
    """
    This class is being setup to standardize the API response across a given project.

    Usage:
        Sample Usage:
        ::
            test = APIResponseClass()
            test.message = "testing message"
            test.status = StatusCode.FAILED

        For setting the data and message:
        ::
            test.data = {
                'some_key': "some_value"
            }
            test.meta  = {
                'some_key': "some_value"
            }

    """

    def __init__(self):
        """
            Initializer to setup default values
        """
        # Default setup
        self.status_code = 200
        self.message = StatusMessage.SUCCESS
        self.data = None
        self.meta = None
        self.error = None

    def get_response(self):
        """
        Get the standardized api output response

        Returns:
            A dict which should be used to respond back on API request wrapping in jsonify

        """

        response_obj = {
            'status_code': self.status_code,
            'message': self.message
        }

        if self.data is not None:
            response_obj['data'] = self.data

        if self.meta is not None:
            response_obj['meta'] = self.meta

        if self.error is not None:
            response_obj['error'] = self.error

        return response_obj
