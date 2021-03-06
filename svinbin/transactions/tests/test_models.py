from mixer.backend.django import mixer

from django.test import TestCase

import workshops.testing_utils as workshops_testing
import sows.testing_utils as sows_testing
from workshops.models import WorkShop, Section, SowSingleCell, PigletsGroupCell, SowGroupCell, \
SowAndPigletsCell
from sows.models import Sow
from transactions.models import Location, SowTransaction


class SowTransactionModelTest(TestCase):
    def setUp(self):
        workshops_testing.create_workshops_sections_and_cells()

    def test_sowtransaction_save(self):
        sow = sows_testing.create_sow_and_put_in_workshop_one(1, '100')
        to_location = Location.objects.create_location(SowSingleCell.objects.get(number='2'))

        transaction = SowTransaction(from_location=sow.location, to_location=to_location,
          sow=sow)

        self.assertEqual(sow.location.sowSingleCell.sow, sow)
        transaction.to_empty_from_location_single_cell
        self.assertEqual(sow.location.sowSingleCell.sow, None)

        transaction.to_fill_to_location_single_cell
        to_location.refresh_from_db()
        self.assertEqual(to_location.sowSingleCell.sow, sow)

        transaction.change_sow_current_location
        sow.refresh_from_db()
        self.assertEqual(sow.location, to_location)


class LocationModelManagerTest(TestCase):
    def setUp(self):
        workshops_testing.create_workshops_sections_and_cells()

    def test_create_location(self):
        location = Location.objects.create_location(WorkShop.objects.get(number=1))
        self.assertEqual(location.workshop.number, 1)

        location = Location.objects.create_location(Section.objects.get(workshop__number=1, \
            number=1))
        self.assertEqual(location.section.number, 1)
        
        location = Location.objects.create_location(SowSingleCell.objects.get(number='1'))
        self.assertEqual(location.sowSingleCell.number, '1')

        location = Location.objects.create_location(SowGroupCell.objects.first())
        self.assertNotEqual(location.sowGroupCell, None)

        location = Location.objects.create_location(SowAndPigletsCell.objects.first())
        self.assertNotEqual(location.sowAndPigletsCell, None)
        

class LocationModelTest(TestCase):
    def setUp(self):
        workshops_testing.create_workshops_sections_and_cells()

    def test_get_location(self):
        workshop = WorkShop.objects.get(number=1)
        location = Location.objects.create_location(workshop)
        self.assertEqual(location.get_location, workshop)

        section = Section.objects.get(workshop__number=1, number=1)
        location = Location.objects.create_location(section)
        self.assertEqual(location.get_location, section)
        
        cell = SowSingleCell.objects.get(number='1')
        location = Location.objects.create_location(cell)
        self.assertEqual(location.get_location, cell)

        cell = SowGroupCell.objects.first()
        location = Location.objects.create_location(cell)
        self.assertEqual(location.get_location, cell)

        cell = PigletsGroupCell.objects.first()
        location = Location.objects.create_location(cell)
        self.assertEqual(location.get_location, cell)

        cell = SowAndPigletsCell.objects.first()
        location = Location.objects.create_location(cell)
        self.assertEqual(location.get_location, cell)

    def test_get_workshop(self):
        workshop = WorkShop.objects.get(number=1)
        location = Location.objects.create_location(workshop)
        self.assertEqual(location.get_workshop, workshop)

        section = Section.objects.get(workshop__number=1, number=1)
        location = Location.objects.create_location(section)
        self.assertEqual(location.get_workshop, workshop)
        
        cell = SowSingleCell.objects.get(number='1')
        location = Location.objects.create_location(cell)
        self.assertEqual(location.get_workshop, workshop)

        cell = SowGroupCell.objects.first()
        location = Location.objects.create_location(cell)
        self.assertEqual(location.get_workshop, cell.section.workshop)

        cell = PigletsGroupCell.objects.first()
        location = Location.objects.create_location(cell)
        self.assertEqual(location.get_workshop, cell.section.workshop)

        cell = SowAndPigletsCell.objects.first()
        location = Location.objects.create_location(cell)
        self.assertEqual(location.get_workshop, cell.section.workshop)