from __future__ import annotations
from datetime import datetime
import json
from typing import Optional
from pydantic import BaseModel


class VehicleInsuranceCostDetails(BaseModel):
    annual_total: Optional[float]
    payable_by_date: Optional[str]

    @staticmethod
    def empty():
        return VehicleInsuranceCostDetails(
            annual_total=0,
            payable_by_date=datetime.now().strftime('%Y-%m-%d')
        )

    def to_dict(self):
        return {
            "annual_total": self.annual_total,
            "payable_by_date": self.payable_by_date
        }


class VehicleInsuranceRenewalDetails(BaseModel):
    renewal_notification_date: Optional[str]
    renewal_due_date: Optional[str]

    @staticmethod
    def empty():
        return VehicleInsuranceRenewalDetails(
            renewal_notification_date=datetime.now().strftime('%Y-%m-%d'),
            renewal_due_date=datetime.now().strftime('%Y-%m-%d')
        )

    def to_dict(self):
        return {
            "renewal_notification_date": self.renewal_notification_date,
            "renewal_due_date": self.renewal_due_date
        }


class VehicleInsurancePersonDetails(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    date_of_birth: Optional[str]
    address: Optional[str]
    email_address: Optional[str]
    total_years_of_residence_in_uk: Optional[int]
    driving_license_number: Optional[str]

    @staticmethod
    def empty():
        return VehicleInsurancePersonDetails(
            first_name='',
            last_name='',
            date_of_birth=datetime.now().strftime('%Y-%m-%d'),
            address='',
            email_address='',
            total_years_of_residence_in_uk=0,
            driving_license_number=''
        )

    def to_dict(self):
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "date_of_birth": self.date_of_birth,
            "address": self.address,
            "email_address": self.email_address,
            "total_years_of_residence_in_uk": self.total_years_of_residence_in_uk,
            "driving_license_number": self.driving_license_number
        }


class VehicleInsuranceVehicleDetails(BaseModel):
    registration_number: Optional[str]
    make: Optional[str]
    model: Optional[str]
    year: Optional[int]
    value: Optional[float]

    @staticmethod
    def empty():
        return VehicleInsuranceVehicleDetails(
            registration_number='',
            make='',
            model='',
            year=2024,
            value=0.0
        )

    def to_dict(self):
        return {
            "registration_number": self.registration_number,
            "make": self.make,
            "model": self.model,
            "year": self.year,
            "value": self.value
        }


class VehicleInsuranceExcessDetails(BaseModel):
    compulsory: Optional[float]
    voluntary: Optional[float]
    unapproved_repair_penalty: Optional[float]

    @staticmethod
    def empty():
        return VehicleInsuranceExcessDetails(
            compulsory=0.0,
            voluntary=0.0,
            unapproved_repair_penalty=0.0
        )

    def to_dict(self):
        return {
            "compulsory": self.compulsory,
            "voluntary": self.voluntary,
            "unapproved_repair_penalty": self.unapproved_repair_penalty
        }


class VehicleInsurancePolicy(BaseModel):
    policy_number: Optional[str]
    cost: Optional[VehicleInsuranceCostDetails]
    renewal: Optional[VehicleInsuranceRenewalDetails]
    effective_from: Optional[str]
    effective_to: Optional[str]
    last_date_to_cancel: Optional[str]
    policyholder: Optional[VehicleInsurancePersonDetails]
    vehicle: Optional[VehicleInsuranceVehicleDetails]
    accident_excess: Optional[VehicleInsuranceExcessDetails]
    fire_and_theft_excess: Optional[VehicleInsuranceExcessDetails]

    @staticmethod
    def empty():
        return VehicleInsurancePolicy(
            policy_number='',
            cost=VehicleInsuranceCostDetails.empty(),
            renewal=VehicleInsuranceRenewalDetails.empty(),
            effective_from=datetime.now().strftime('%Y-%m-%d'),
            effective_to=datetime.now().strftime('%Y-%m-%d'),
            last_date_to_cancel=datetime.now().strftime('%Y-%m-%d'),
            policyholder=VehicleInsurancePersonDetails.empty(),
            vehicle=VehicleInsuranceVehicleDetails.empty(),
            accident_excess=VehicleInsuranceExcessDetails.empty(),
            fire_and_theft_excess=VehicleInsuranceExcessDetails.empty()
        )

    @staticmethod
    def empty_json():
        return json.dumps(VehicleInsurancePolicy.empty().to_dict())

    @staticmethod
    def from_json(json_str: str):
        json_content = json.loads(json_str)

        policy_number = json_content.get("policy_number", None)
        cost = json_content.get("cost", None)
        renewal = json_content.get("renewal", None)
        effective_from = json_content.get("effective_from", None)
        effective_to = json_content.get("effective_to", None)
        last_date_to_cancel = json_content.get("last_date_to_cancel", None)
        policyholder = json_content.get("policyholder", None)
        vehicle = json_content.get("vehicle", None)
        accident_excess = json_content.get("accident_excess", None)
        fire_and_theft_excess = json_content.get("fire_and_theft_excess", None)

        cost = VehicleInsuranceCostDetails(
            cost.get("annual_total", None), cost.get("payable_by_date", None)) if cost is not None else None

        renewal = VehicleInsuranceRenewalDetails(
            renewal.get("renewal_notification_date", None), renewal.get("renewal_due_date", None)) if renewal is not None else None

        policyholder = VehicleInsurancePersonDetails(
            policyholder.get("first_name", None), policyholder.get("last_name", None), policyholder.get("date_of_birth", None), policyholder.get("address", None), policyholder.get("email_address", None), policyholder.get("total_years_of_residence_in_uk", None), policyholder.get("driving_license_number", None)) if policyholder is not None else None

        vehicle = VehicleInsuranceVehicleDetails(
            vehicle.get("registration_number", None), vehicle.get("make", None), vehicle.get("model", None), vehicle.get("year", None), vehicle.get("value", None)) if vehicle is not None else None

        accident_excess = VehicleInsuranceExcessDetails(
            accident_excess.get("compulsory", None), accident_excess.get("voluntary", None), accident_excess.get("unapproved_repair_penalty", None)) if accident_excess is not None else None

        fire_and_theft_excess = VehicleInsuranceExcessDetails(
            fire_and_theft_excess.get("compulsory", None), fire_and_theft_excess.get("voluntary", None), fire_and_theft_excess.get("unapproved_repair_penalty", None)) if fire_and_theft_excess is not None else None

        return VehicleInsurancePolicy(policy_number, cost, renewal, effective_from, effective_to, last_date_to_cancel, policyholder, vehicle, accident_excess, fire_and_theft_excess)

    def to_dict(self):
        return {
            "policy_number": self.policy_number,
            "cost": self.cost.to_dict(),
            "renewal": self.renewal.to_dict(),
            "effective_from": self.effective_from,
            "effective_to": self.effective_to,
            "last_date_to_cancel": self.last_date_to_cancel,
            "policyholder": self.policyholder.to_dict(),
            "vehicle": self.vehicle.to_dict(),
            "accident_excess": self.accident_excess.to_dict(),
            "fire_and_theft_excess": self.fire_and_theft_excess.to_dict()
        }


class VehicleInsurancePolicyEvaluator:
    def __init__(self, expected: VehicleInsurancePolicy):
        self.expected = expected

    def evaluate(self, actual: Optional[VehicleInsurancePolicy]):
        def compare_cost(expected_cost: VehicleInsuranceCostDetails, actual_cost: Optional[VehicleInsuranceCostDetails]):
            cost_accuracy = {
                "annual_total": 0,
                "payable_by_date": 0,
                "overall": 0
            }

            if actual_cost is None:
                return cost_accuracy

            cost_accuracy["annual_total"] = 1 if expected_cost.annual_total == actual_cost.annual_total else 0
            cost_accuracy["payable_by_date"] = 1 if (expected_cost.payable_by_date or '').lower() == (
                actual_cost.payable_by_date or '').lower() else 0
            cost_accuracy["overall"] = (cost_accuracy["annual_total"] +
                                        cost_accuracy["payable_by_date"]) / 2

            return cost_accuracy

        def compare_renewal(expected_renewal: VehicleInsuranceRenewalDetails, actual_renewal: Optional[VehicleInsuranceRenewalDetails]):
            renewal_accuracy = {
                "renewal_notification_date": 0,
                "renewal_due_date": 0,
                "overall": 0
            }

            if actual_renewal is None:
                return renewal_accuracy

            renewal_accuracy["renewal_notification_date"] = 1 if (expected_renewal.renewal_notification_date or '').lower() == (
                actual_renewal.renewal_notification_date or '').lower() else 0
            renewal_accuracy["renewal_due_date"] = 1 if (expected_renewal.renewal_due_date or '').lower() == (
                actual_renewal.renewal_due_date or '').lower() else 0
            renewal_accuracy["overall"] = (renewal_accuracy["renewal_notification_date"] +
                                           renewal_accuracy["renewal_due_date"]) / 2

            return renewal_accuracy

        def compare_person(expected_person: VehicleInsurancePersonDetails, actual_person: Optional[VehicleInsurancePersonDetails]):
            person_accuracy = {
                "first_name": 0,
                "last_name": 0,
                "date_of_birth": 0,
                "address": 0,
                "email_address": 0,
                "total_years_of_residence_in_uk": 0,
                "driving_license_number": 0,
                "overall": 0
            }

            if actual_person is None:
                return person_accuracy

            person_accuracy["first_name"] = 1 if (expected_person.first_name or '').lower() == (
                actual_person.first_name or '').lower() else 0
            person_accuracy["last_name"] = 1 if (expected_person.last_name or '').lower() == (
                actual_person.last_name or '').lower() else 0
            person_accuracy["date_of_birth"] = 1 if (expected_person.date_of_birth or '').lower() == (
                actual_person.date_of_birth or '').lower() else 0
            person_accuracy["address"] = 1 if (expected_person.address or '').lower() == (
                actual_person.address or '').lower() else 0
            person_accuracy["email_address"] = 1 if (expected_person.email_address or '').lower() == (
                actual_person.email_address or '').lower() else 0
            person_accuracy["total_years_of_residence_in_uk"] = 1 if expected_person.total_years_of_residence_in_uk == actual_person.total_years_of_residence_in_uk else 0
            person_accuracy["driving_license_number"] = 1 if (expected_person.driving_license_number or '').lower() == (
                actual_person.driving_license_number or '').lower() else 0
            person_accuracy["overall"] = (person_accuracy["first_name"] + person_accuracy["last_name"] + person_accuracy["date_of_birth"] + person_accuracy["address"] +
                                          person_accuracy["email_address"] + person_accuracy["total_years_of_residence_in_uk"] + person_accuracy["driving_license_number"]) / 7
            return person_accuracy

        def compare_vehicle(expected_vehicle: VehicleInsuranceVehicleDetails, actual_vehicle: Optional[VehicleInsuranceVehicleDetails]):
            vehicle_accuracy = {
                "registration_number": 0,
                "make": 0,
                "model": 0,
                "year": 0,
                "value": 0,
                "overall": 0
            }

            if actual_vehicle is None:
                return vehicle_accuracy

            vehicle_accuracy["registration_number"] = 1 if (expected_vehicle.registration_number or '').lower() == (
                actual_vehicle.registration_number or '').lower() else 0
            vehicle_accuracy["make"] = 1 if (expected_vehicle.make or '').lower() == (
                actual_vehicle.make or '').lower() else 0
            vehicle_accuracy["model"] = 1 if (expected_vehicle.model or '').lower() == (
                actual_vehicle.model or '').lower() else 0
            vehicle_accuracy["year"] = 1 if expected_vehicle.year == actual_vehicle.year else 0
            vehicle_accuracy["value"] = 1 if expected_vehicle.value == actual_vehicle.value else 0
            vehicle_accuracy["overall"] = (vehicle_accuracy["registration_number"] + vehicle_accuracy["make"] +
                                           vehicle_accuracy["model"] + vehicle_accuracy["year"] + vehicle_accuracy["value"]) / 5
            return vehicle_accuracy

        def compare_excess(expected_excess: VehicleInsuranceExcessDetails, actual_excess: Optional[VehicleInsuranceExcessDetails]):
            excess_accuracy = {
                "compulsory": 0,
                "voluntary": 0,
                "unapproved_repair_penalty": 0,
                "overall": 0
            }

            if actual_excess is None:
                return excess_accuracy

            excess_accuracy["compulsory"] = 1 if expected_excess.compulsory == actual_excess.compulsory else 0
            excess_accuracy["voluntary"] = 1 if expected_excess.voluntary == actual_excess.voluntary else 0
            excess_accuracy["unapproved_repair_penalty"] = 1 if expected_excess.unapproved_repair_penalty == actual_excess.unapproved_repair_penalty else 0
            excess_accuracy["overall"] = (
                excess_accuracy["compulsory"] + excess_accuracy["voluntary"] + excess_accuracy["unapproved_repair_penalty"]) / 3
            return excess_accuracy

        policy_accuracy = {
            "policy_number": 0,
            "cost": 0,
            "renewal": 0,
            "effective_from": 0,
            "effective_to": 0,
            "last_date_to_cancel": 0,
            "policyholder": 0,
            "vehicle": 0,
            "accident_excess": 0,
            "fire_and_theft_excess": 0,
            "overall": 0
        }

        if actual is None:
            return policy_accuracy

        policy_accuracy["policy_number"] = 1 if (self.expected.policy_number or '').lower() == (
            actual.policy_number or '').lower() else 0

        if actual.cost is None:
            policy_accuracy["cost"] = {
                "overall": 1 if self.expected.cost is None else 0
            }
        else:
            policy_accuracy["cost"] = compare_cost(
                self.expected.cost, actual.cost)

        if actual.renewal is None:
            policy_accuracy["renewal"] = {
                "overall": 1 if self.expected.renewal is None else 0
            }
        else:
            policy_accuracy["renewal"] = compare_renewal(
                self.expected.renewal, actual.renewal)

        policy_accuracy["effective_from"] = 1 if (self.expected.effective_from or '').lower() == (
            actual.effective_from or '').lower() else 0
        policy_accuracy["effective_to"] = 1 if (self.expected.effective_to or '').lower() == (
            actual.effective_to or '').lower() else 0
        policy_accuracy["last_date_to_cancel"] = 1 if (self.expected.last_date_to_cancel or '').lower() == (
            actual.last_date_to_cancel or '').lower() else 0

        if actual.policyholder is None:
            policy_accuracy["policyholder"] = {
                "overall": 1 if self.expected.policyholder is None else 0
            }
        else:
            policy_accuracy["policyholder"] = compare_person(
                self.expected.policyholder, actual.policyholder)

        if actual.vehicle is None:
            policy_accuracy["vehicle"] = {
                "overall": 1 if self.expected.vehicle is None else 0
            }
        else:
            policy_accuracy["vehicle"] = compare_vehicle(
                self.expected.vehicle, actual.vehicle)

        if actual.accident_excess is None:
            policy_accuracy["accident_excess"] = {
                "overall": 1 if self.expected.accident_excess is None else 0
            }
        else:
            policy_accuracy["accident_excess"] = compare_excess(
                self.expected.accident_excess, actual.accident_excess)

        if actual.fire_and_theft_excess is None:
            policy_accuracy["fire_and_theft_excess"] = {
                "overall": 1 if self.expected.fire_and_theft_excess is None else 0
            }
        else:
            policy_accuracy["fire_and_theft_excess"] = compare_excess(
                self.expected.fire_and_theft_excess, actual.fire_and_theft_excess)

        policy_accuracy["overall"] = (policy_accuracy["policy_number"] + policy_accuracy["cost"]["overall"] + policy_accuracy["renewal"]["overall"] + policy_accuracy["effective_from"] + policy_accuracy["effective_to"] +
                                      policy_accuracy["last_date_to_cancel"] + policy_accuracy["policyholder"]["overall"] + policy_accuracy["vehicle"]["overall"] + policy_accuracy["accident_excess"]["overall"] + policy_accuracy["fire_and_theft_excess"]["overall"]) / 10

        return policy_accuracy
