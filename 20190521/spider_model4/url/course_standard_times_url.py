class CourseStandardTimesUrl(object):

    BASE_URL = 'https://racing.hkjc.com/racing/english/racing-info/racing_course_time.asp'

    EXPORT_TABLE = 'ii_course_standard_times'

    def getUrl(self):
        return self.BASE_URL
