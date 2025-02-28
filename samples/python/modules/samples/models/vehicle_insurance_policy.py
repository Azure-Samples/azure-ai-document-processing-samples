from __future__ import annotations
from datetime import datetime
import json
from typing import Optional
from pydantic import BaseModel, Field


class VehicleInsuranceCostDetails(BaseModel):
    """
    A class representing the cost details of a vehicle insurance policy.

    Attributes:
        annual_total: The annual total cost of the vehicle insurance policy.
        payable_by_date: The date by which the vehicle insurance policy must be paid.
    """

    annual_total: Optional[float] = Field(
        description='The annual total cost of the vehicle insurance policy.'
    )
    payable_by_date: Optional[str] = Field(
        description='The date by which the vehicle insurance policy must be paid.'
    )

    @staticmethod
    def example():
        """
        Returns an empty example VehicleInsuranceCostDetails object with default values.

        Returns:
            VehicleInsuranceCostDetails: An empty VehicleInsuranceCostDetails object.
        """

        return VehicleInsuranceCostDetails(
            annual_total=0,
            payable_by_date=datetime.now().strftime('%Y-%m-%d')
        )


class VehicleInsuranceRenewalDetails(BaseModel):
    """
    A class representing the renewal details of a vehicle insurance policy.

    Attributes:
        renewal_notification_date: The date on which the renewal notification is sent.
        last_date_to_renew: The last date before renewal is required.
    """

    renewal_notification_date: Optional[str] = Field(
        description='The date on which the renewal notification is sent.'
    )
    last_date_to_renew: Optional[str] = Field(
        description='The last date before renewal is required.'
    )

    @staticmethod
    def example():
        """
        Returns an empty example VehicleInsuranceRenewalDetails object with default values.

        Returns:
            VehicleInsuranceRenewalDetails: An empty VehicleInsuranceRenewalDetails object.
        """

        return VehicleInsuranceRenewalDetails(
            renewal_notification_date=datetime.now().strftime('%Y-%m-%d'),
            last_date_to_renew=datetime.now().strftime('%Y-%m-%d')
        )


class VehicleInsurancePersonDetails(BaseModel):
    """
    A class representing the person details of a vehicle insurance policy.

    Attributes:
        first_name: The first name of the person.
        last_name: The last name of the person.
        date_of_birth: The date of birth of the person.
        address: The current address of the person.
        email_address: The email address of the person.
        total_years_of_residence_in_uk: The total years the person has resided in the UK.
        driving_license_number: The driving license number of the person.
    """

    first_name: Optional[str] = Field(
        description='The first name of the person.'
    )
    last_name: Optional[str] = Field(
        description='The last name or surname of the person.'
    )
    date_of_birth: Optional[str] = Field(
        description='The date of birth of the person.'
    )
    address: Optional[str] = Field(
        description='The current address of the person.'
    )
    email_address: Optional[str] = Field(
        description='The email address of the person.'
    )
    total_years_of_residence_in_uk: Optional[int] = Field(
        description='The total years the person has resided in the UK.'
    )
    driving_license_number: Optional[str] = Field(
        description='The driving license number of the person.'
    )

    @staticmethod
    def example():
        """
        Returns an empty example VehicleInsurancePersonDetails object with default values.

        Returns:
            VehicleInsurancePersonDetails: An empty VehicleInsurancePersonDetails object.
        """

        return VehicleInsurancePersonDetails(
            first_name='',
            last_name='',
            date_of_birth=datetime.now().strftime('%Y-%m-%d'),
            address='',
            email_address='',
            total_years_of_residence_in_uk=0,
            driving_license_number=''
        )


class VehicleInsuranceVehicleDetails(BaseModel):
    """
    A class representing the vehicle details of a vehicle insurance policy.

    Attributes:
        registration_number: The registration number of the vehicle.
        make: The make of the vehicle.
        model: The model of the vehicle.
        year: The year the vehicle was manufactured.
        value: The current value of the vehicle.
    """

    registration_number: Optional[str] = Field(
        description='The registration number of the vehicle.'
    )
    make: Optional[str] = Field(
        description='The make of the vehicle.'
    )
    model: Optional[str] = Field(
        description='The model of the vehicle.'
    )
    year: Optional[int] = Field(
        description='The year the vehicle was manufactured.'
    )
    value: Optional[float] = Field(
        description='The current value of the vehicle.'
    )

    @staticmethod
    def example():
        """
        Returns an empty example VehicleInsuranceVehicleDetails object with default values.

        Returns:
            VehicleInsuranceVehicleDetails: An empty VehicleInsuranceVehicleDetails object.
        """

        return VehicleInsuranceVehicleDetails(
            registration_number='',
            make='',
            model='',
            year=2024,
            value=0.0
        )


class VehicleInsuranceExcessDetails(BaseModel):
    """
    A class representing the excess details of a vehicle insurance policy.

    Attributes:
        compulsory: The compulsory excess amount.
        voluntary: The voluntary excess amount.
        unapproved_repair_penalty: The penalty amount for repairs by unapproved repairers.
    """

    compulsory: Optional[int] = Field(
        description='The compulsory excess amount.'
    )
    voluntary: Optional[int] = Field(
        description='The voluntary excess amount.'
    )
    unapproved_repair_penalty: Optional[int] = Field(
        description='The penalty amount for repairs by unapproved repairers.'
    )

    @staticmethod
    def example():
        """
        Returns an empty example VehicleInsuranceExcessDetails object with default values.

        Returns:
            VehicleInsuranceExcessDetails: An empty VehicleInsuranceExcessDetails object.
        """

        return VehicleInsuranceExcessDetails(
            compulsory=0,
            voluntary=0,
            unapproved_repair_penalty=0
        )


class VehicleInsurancePolicy(BaseModel):
    """
    A class representing a vehicle insurance policy.

    Attributes:
        policy_number: The policy number of the vehicle insurance policy.
        cost: The cost details of the vehicle insurance policy.
        renewal: The renewal details of the vehicle insurance policy.
        effective_from: The effective date from which the vehicle insurance policy is valid.
        effective_to: The effective date to which the vehicle insurance policy is valid.
        last_date_to_cancel: The last date to cancel the vehicle insurance policy.
        policyholder: The person details of the policyholder.
        vehicle: The vehicle details of the policy.
        accident_excess: The excess costs for accidents.
        fire_and_theft_excess: The excess costs for fire and theft.
    """

    policy_number: Optional[str] = Field(
        description='The policy number of the vehicle insurance policy.'
    )
    cost: Optional[VehicleInsuranceCostDetails] = Field(
        description='The cost details of the vehicle insurance policy.'
    )
    renewal: Optional[VehicleInsuranceRenewalDetails] = Field(
        description='The renewal details of the vehicle insurance policy.'
    )
    effective_from: Optional[str] = Field(
        description='The effective date from which the vehicle insurance policy is valid.'
    )
    effective_to: Optional[str] = Field(
        description='The effective date to which the vehicle insurance policy is valid.'
    )
    last_date_to_cancel: Optional[str] = Field(
        description='The last date to cancel the vehicle insurance policy.'
    )
    policyholder: Optional[VehicleInsurancePersonDetails] = Field(
        description='The person details of the policyholder.'
    )
    vehicle: Optional[VehicleInsuranceVehicleDetails] = Field(
        description='The vehicle details of the policy.'
    )
    accident_excess: Optional[VehicleInsuranceExcessDetails] = Field(
        description='The excess costs for accidents.'
    )
    fire_and_theft_excess: Optional[VehicleInsuranceExcessDetails] = Field(
        description='The excess costs for fire and theft.'
    )

    @staticmethod
    def example():
        """
        Returns an empty example VehicleInsurancePolicy object with default values.

        Returns:
            VehicleInsurancePolicy: An empty VehicleInsurancePolicy object.
        """

        return VehicleInsurancePolicy(
            policy_number='',
            cost=VehicleInsuranceCostDetails.example(),
            renewal=VehicleInsuranceRenewalDetails.example(),
            effective_from=datetime.now().strftime('%Y-%m-%d'),
            effective_to=datetime.now().strftime('%Y-%m-%d'),
            last_date_to_cancel=datetime.now().strftime('%Y-%m-%d'),
            policyholder=VehicleInsurancePersonDetails.example(),
            vehicle=VehicleInsuranceVehicleDetails.example(),
            accident_excess=VehicleInsuranceExcessDetails.example(),
            fire_and_theft_excess=VehicleInsuranceExcessDetails.example()
        )

    @staticmethod
    def from_json(json_str: str):
        """
        Converts a JSON string to a VehicleInsurancePolicy object.

        Args:
            json_str: The JSON string to convert.

        Returns:
            VehicleInsurancePolicy: The VehicleInsurancePolicy object.
        """

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
            renewal.get("renewal_notification_date", None), renewal.get("last_date_to_renew", None)) if renewal is not None else None

        policyholder = VehicleInsurancePersonDetails(
            policyholder.get("first_name", None), policyholder.get("last_name", None), policyholder.get("date_of_birth", None), policyholder.get("address", None), policyholder.get("email_address", None), policyholder.get("total_years_of_residence_in_uk", None), policyholder.get("driving_license_number", None)) if policyholder is not None else None

        vehicle = VehicleInsuranceVehicleDetails(
            vehicle.get("registration_number", None), vehicle.get("make", None), vehicle.get("model", None), vehicle.get("year", None), vehicle.get("value", None)) if vehicle is not None else None

        accident_excess = VehicleInsuranceExcessDetails(
            accident_excess.get("compulsory", None), accident_excess.get("voluntary", None), accident_excess.get("unapproved_repair_penalty", None)) if accident_excess is not None else None

        fire_and_theft_excess = VehicleInsuranceExcessDetails(
            fire_and_theft_excess.get("compulsory", None), fire_and_theft_excess.get("voluntary", None), fire_and_theft_excess.get("unapproved_repair_penalty", None)) if fire_and_theft_excess is not None else None

        return VehicleInsurancePolicy(policy_number, cost, renewal, effective_from, effective_to, last_date_to_cancel, policyholder, vehicle, accident_excess, fire_and_theft_excess)
