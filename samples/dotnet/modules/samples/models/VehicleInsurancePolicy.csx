using System.ComponentModel;

public class VehicleInsuranceCostDetails
{
    [Description("The annual total cost of the vehicle insurance policy.")]
    public float? AnnualTotal { get; set; }

    [Description("The date by which the vehicle insurance policy must be paid.")]
    public string? PayableByDate { get; set; }
}

public class VehicleInsuranceRenewalDetails
{
    [Description("The date on which the renewal notification is sent.")]
    public string? RenewalNotificationDate { get; set; }

    [Description("The last date before renewal is required.")]
    public string? LastDateToRenew { get; set; }
}

public class VehicleInsurancePersonDetails
{
    [Description("The first name of the person.")]
    public string? FirstName { get; set; }

    [Description("The last name or surname of the person.")]
    public string? LastName { get; set; }

    [Description("The date of birth of the person.")]
    public string? DateOfBirth { get; set; }

    [Description("The current address of the person.")]
    public string? Address { get; set; }

    [Description("The email address of the person.")]
    public string? EmailAddress { get; set; }

    [Description("The total years the person has resided in the UK.")]
    public int? TotalYearsOfResidenceInUK { get; set; }

    [Description("The driving license number of the person.")]
    public string? DrivingLicenseNumber { get; set; }
}

public class VehicleInsuranceVehicleDetails
{
    [Description("The registration number of the vehicle.")]
    public string? RegistrationNumber { get; set; }

    [Description("The make of the vehicle.")]
    public string? Make { get; set; }

    [Description("The model of the vehicle.")]
    public string? Model { get; set; }

    [Description("The year of manufacture of the vehicle.")]
    public int? Year { get; set; }

    [Description("The current value of the vehicle.")]
    public float? Value { get; set; }
}

public class VehicleInsuranceExcessDetails
{
    [Description("The compulsory excess amount.")]
    public int? Compulsory { get; set; }

    [Description("The voluntary excess amount.")]
    public int? Voluntary { get; set; }

    [Description("The penalty amount for repairs by an unapproved repairer.")]
    public int? UnapprovedRepairPenalty { get; set; }
}

public class VehicleInsurancePolicy
{
    [Description("The policy number of the vehicle insurance policy.")]
    public string? PolicyNumber { get; set; }

    [Description("The cost details of the vehicle insurance policy.")]
    public VehicleInsuranceCostDetails? Cost { get; set; }

    [Description("The renewal details of the vehicle insurance policy.")]
    public VehicleInsuranceRenewalDetails? Renewal { get; set; }

    [Description("The effective date from which the vehicle insurance policy is valid.")]
    public string? EffectiveFrom { get; set; }

    [Description("The effective date until which the vehicle insurance policy is valid.")]
    public string? EffectiveTo { get; set; }

    [Description("The last date by which the vehicle insurance policy can be canceled.")]
    public string? LastDateToCancel { get; set; }

    [Description("The policyholder details of the vehicle insurance policy.")]
    public VehicleInsurancePersonDetails? Policyholder { get; set; }

    [Description("The vehicle details of the vehicle insurance policy.")]
    public VehicleInsuranceVehicleDetails? Vehicle { get; set; }

    [Description("The excess costs for accidents.")]
    public VehicleInsuranceExcessDetails? AccidentExcess { get; set; }

    [Description("The excess costs for fire and theft.")]
    public VehicleInsuranceExcessDetails? FireAndTheftExcess { get; set; }
}
