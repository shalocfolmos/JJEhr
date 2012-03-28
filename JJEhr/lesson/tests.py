from django.test import TestCase

class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)
        #

    #    def test_save_course(self):
    #        p = Course(courseName='test',courseTime=2,startTime=datetime.now(),maxTraineeAmount=2,courseSpeaker='evan')
    #        p.save()

    def test_page(self):
        pageNo = 8
        pageSize = 10
        pageCount = 30
        pre_page_count = 9
        if pageCount < pre_page_count:
            startPageIndex = 1
            endPageIndex = pageCount
        elif pageNo <= (pre_page_count / 2) + 1:
            startPageIndex = 1
            endPageIndex = pre_page_count
        else:
            startPageIndex = pageNo - (pre_page_count / 2)
            endPageIndex = pageNo + ((pre_page_count / 2))
            if endPageIndex >= pageCount:
                endPageIndex = pageCount
                startPageIndex = pageCount - pre_page_count + 1
        self.assertEqual(startPageIndex, 4)
        self.assertEqual(endPageIndex, 12)



