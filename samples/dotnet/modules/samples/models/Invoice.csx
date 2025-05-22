using System.ComponentModel;

/// <summary>
/// A class representing a currency in an invoice.
/// </summary>
[Description("A class representing a currency in an invoice.")]
public class InvoiceCurrency
{
    /// <summary>
    /// Gets or sets the currency code, e.g. USD.
    /// </summary>
    [Description("Currency code, e.g. USD")]
    public string? CurrencyCode { get; set; }

    /// <summary>
    /// Gets or sets the currency amount, e.g. 100.00.
    /// </summary>
    [Description("Currency amount, e.g. 100.00")]
    public float? Amount { get; set; }
}

/// <summary>
/// A class representing an address in an invoice.
/// </summary>
[Description("A class representing an address in an invoice.")]
public class InvoiceAddress
{
    /// <summary>
    /// Gets or sets the street address, e.g. 123 456th St.
    /// </summary>
    [Description("Street address, e.g. 123 456th St.")]
    public string? Street { get; set; }

    /// <summary>
    /// Gets or sets the name of the city, town, village, etc., e.g. New York.
    /// </summary>
    [Description("Name of city, town, village, etc., e.g. New York")]
    public string? City { get; set; }

    /// <summary>
    /// Gets or sets the name of the state or local administrative division, e.g. NY.
    /// </summary>
    [Description("Name of State or local administrative division, e.g. NY")]
    public string? State { get; set; }

    /// <summary>
    /// Gets or sets the postal code, e.g. 10001.
    /// </summary>
    [Description("Postal code, e.g. 10001")]
    public string? PostalCode { get; set; }

    /// <summary>
    /// Gets or sets the country, e.g. USA.
    /// </summary>
    [Description("Country, e.g. USA")]
    public string? Country { get; set; }
}

/// <summary>
/// A class representing a signature in an invoice.
/// </summary>
[Description("A class representing a signature in an invoice.")]
public class InvoiceSignature
{
    /// <summary>
    /// Gets or sets the name of the person who signed the invoice, e.g. John Doe.
    /// </summary>
    [Description("Name of the person who signed the invoice, e.g. John Doe")]
    public string? Signatory { get; set; }

    /// <summary>
    /// Gets or sets the date when the invoice was signed, e.g. 2019-11-15.
    /// </summary>
    [Description("Date when the invoice was signed, e.g. 2019-11-15")]
    public string? Date { get; set; }

    /// <summary>
    /// Gets or sets a value indicating whether the invoice has a written signature.
    /// </summary>
    [Description("Indicates if the invoice has a written signature, e.g. true")]
    public bool? HasWrittenSignature { get; set; }
}

/// <summary>
/// A class representing a line item in an invoice.
/// </summary>
[Description("A class representing a line item in an invoice.")]
public class InvoiceItem
{
    /// <summary>
    /// Gets or sets the product code, product number, or SKU for the line item.
    /// </summary>
    [Description("Product code, product number, or SKU for the line item, e.g. A123")]
    public string? ProductCode { get; set; }

    /// <summary>
    /// Gets or sets the text description for the line item.
    /// </summary>
    [Description("Text description for the line item, e.g. Consulting service")]
    public string? Description { get; set; }

    /// <summary>
    /// Gets or sets the quantity of the line item.
    /// </summary>
    [Description("Quantity for the line item, e.g. 2")]
    public int? Quantity { get; set; }

    /// <summary>
    /// Gets or sets the tax amount applied to the line item.
    /// </summary>
    [Description("Tax amount applied to the line item, e.g. 6.00")]
    public InvoiceCurrency? Tax { get; set; }

    /// <summary>
    /// Gets or sets the net or gross price of one unit of the line item.
    /// </summary>
    [Description("Net or gross price of one unit of the line item, e.g. 30.00")]
    public InvoiceCurrency? UnitPrice { get; set; }

    /// <summary>
    /// Gets or sets the total charges for the line item.
    /// </summary>
    [Description("Total charges for the line item, e.g. 60.00")]
    public InvoiceCurrency? Total { get; set; }
}

/// <summary>
/// A class representing an invoice.
/// </summary>
[Description("A class representing an invoice.")]
public class Invoice
{
    /// <summary>
    /// Gets or sets the name of the customer being invoiced.
    /// </summary>
    [Description("Name of the customer being invoiced, e.g. Microsoft Corp")]
    public string? CustomerName { get; set; }

    /// <summary>
    /// Gets or sets the government tax ID of the customer.
    /// </summary>
    [Description("Government tax ID of the customer, e.g. 765432-1")]
    public string? CustomerTaxId { get; set; }

    /// <summary>
    /// Gets or sets the full mailing address of the customer.
    /// </summary>
    [Description("Full mailing address of the customer, e.g. 123 Other St., Redmond, WA, 98052, USA")]
    public InvoiceAddress? CustomerAddress { get; set; }

    /// <summary>
    /// Gets or sets the explicit shipping address for the customer.
    /// </summary>
    [Description("Explicit full shipping address for the customer (null if the same as customer address), e.g. 123 Ship St., Redmond, WA, 98052, USA")]
    public InvoiceAddress? ShippingAddress { get; set; }

    /// <summary>
    /// Gets or sets the purchase order reference number.
    /// </summary>
    [Description("Purchase order reference number, e.g. PO-3333")]
    public string? PurchaseOrder { get; set; }

    /// <summary>
    /// Gets or sets the reference ID or invoice number for the invoice.
    /// </summary>
    [Description("Reference ID or invoice number for the invoice, e.g. INV-100")]
    public string? InvoiceId { get; set; }

    /// <summary>
    /// Gets or sets the date the invoice was issued.
    /// </summary>
    [Description("Date the invoice was issued, e.g., 2019-11-15")]
    public string? InvoiceDate { get; set; }

    /// <summary>
    /// Gets or sets the date payment for the invoice is due.
    /// </summary>
    [Description("Date payment for the invoice is due, e.g., 2019-12-15")]
    public string? DueDate { get; set; }

    /// <summary>
    /// Gets or sets the name of the vendor/supplier who created the invoice.
    /// </summary>
    [Description("Name of the vendor/supplier who created the invoice, e.g. CONTOSO LTD.")]
    public string? VendorName { get; set; }

    /// <summary>
    /// Gets or sets the full mailing address of the vendor/supplier.
    /// </summary>
    [Description("Full mailing address of the vendor/supplier, e.g. 123 456th St, New York, NY, 10001, USA")]
    public InvoiceAddress? VendorAddress { get; set; }

    /// <summary>
    /// Gets or sets the government tax ID of the vendor/supplier.
    /// </summary>
    [Description("Government tax ID of the vendor/supplier, e.g. 123456-7")]
    public string? VendorTaxId { get; set; }

    /// <summary>
    /// Gets or sets the explicit remittance or payment address for the vendor/supplier.
    /// </summary>
    [Description("Explicit full remittance or payment address for where the payment should be sent (null if the same as vendor address), e.g. 123 Remit St, New York, NY, 10001, USA")]
    public InvoiceAddress? RemittanceAddress { get; set; }

    /// <summary>
    /// Gets or sets the subtotal charges for the invoice before discounts and taxes.
    /// </summary>
    [Description("Subtotal charges for the invoice before discounts and taxes, e.g. 100.00")]
    public InvoiceCurrency? Subtotal { get; set; }

    /// <summary>
    /// Gets or sets the total discount applied to the invoice.
    /// </summary>
    [Description("Total discount applied to the invoice, e.g. 5.00")]
    public InvoiceCurrency? TotalDiscount { get; set; }

    /// <summary>
    /// Gets or sets the total tax applied to the invoice.
    /// </summary>
    [Description("Total tax applied to the invoice, e.g. 5.00")]
    public InvoiceCurrency? TotalTax { get; set; }

    /// <summary>
    /// Gets or sets the total charges for the invoice after discounts and taxes.
    /// </summary>
    [Description("Total charges for the invoice after discounts and taxes, e.g. 100.00")]
    public InvoiceCurrency? InvoiceTotal { get; set; }

    /// <summary>
    /// Gets or sets the terms of payment for the invoice.
    /// </summary>
    [Description("Terms of payment for the invoice, e.g. Net30")]
    public string? PaymentTerm { get; set; }

    /// <summary>
    /// Gets or sets the list of line items in the invoice.
    /// </summary>
    [Description("List of line items in the invoice")]
    public List<InvoiceItem>? Items { get; set; }

    /// <summary>
    /// Gets or sets the signature of the customer.
    /// </summary>
    [Description("Signature of the customer, e.g. John Doe")]
    public InvoiceSignature? CustomerSignature { get; set; }
}
