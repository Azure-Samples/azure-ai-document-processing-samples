using System.ComponentModel;

public class InvoiceAddress
{
    /// <summary>
    /// Gets or sets the street address, e.g. 123 Main St.
    /// </summary>
    [Description("Street address, e.g. 123 Main St.")]
    public string? Street { get; set; }

    /// <summary>
    /// Gets or sets the city, e.g. New York.
    /// </summary>
    [Description("City, e.g. New York.")]
    public string? City { get; set; }

    /// <summary>
    /// Gets or sets the state, e.g. NY.
    /// </summary>
    [Description("State, e.g. NY.")]
    public string? State { get; set; }

    /// <summary>
    /// Gets or sets the postal code, e.g. 10001.
    /// </summary>
    [Description("Postal code, e.g. 10001.")]
    public string? PostalCode { get; set; }

    /// <summary>
    /// Gets or sets the country, e.g. USA.
    /// </summary>
    [Description("Country, e.g. USA.")]
    public string? Country { get; set; }
}

public class InvoiceSignature
{
    /// <summary>
    /// Gets or sets the name of the person who signed the invoice.
    /// </summary>
    [Description("Name of the person who signed the invoice.")]
    public string? Signatory { get; set; }

    /// <summary>
    /// Gets or sets a value indicating whether the invoice is by the signatory.
    /// </summary>
    [Description("Indicates whether the invoice is by the signatory.")]
    public bool? IsSigned { get; set; }
}

public class InvoiceItem
{
    /// <summary>
    /// Gets or sets the code of the product.
    /// </summary>
    [Description("Product code, product number, or SKU associated with the line item, e.g. SKU-123")]
    public string? ProductCode { get; set; }

    /// <summary>
    /// Gets or sets the description of the product.
    /// </summary>
    [Description("Description of the line item, e.g. Product A")]
    public string? ProductDescription { get; set; }

    /// <summary>
    /// Gets or sets the quantity of the product.
    /// </summary>
    [Description("Quantity of the line item")]
    public int? Quantity { get; set; }

    /// <summary>
    /// Gets or sets the tax amount applied to the product.
    /// </summary>
    [Description("Tax amount applied to the line item, e.g. 6.99")]
    public float? Tax { get; set; }

    /// <summary>
    /// Gets or sets the tax rate applied to the product.
    /// </summary>
    [Description("Tax rate applied to the line item, e.g. 18%")]
    public string? TaxRate { get; set; }

    /// <summary>
    /// Gets or sets the net or gross price of one unit of the product.
    /// </summary>
    [Description("Net or gross price of one unit of the line item, e.g. 9.99")]
    public float? UnitPrice { get; set; }

    /// <summary>
    /// Gets or sets the total charges associated with the product.
    /// </summary>
    [Description("Total charges associated with the line item, e.g. 19.98")]
    public float? Total { get; set; }

    /// <summary>
    /// Gets or sets the reason for returning the product.
    /// </summary>
    [Description("Reason for returning the line item, e.g. Damaged")]
    public string? Reason { get; set; }
}

public class Invoice
{
    /// <summary>
    /// Gets or sets the name of the customer.
    /// </summary>
    [Description("Name of the customer being invoiced, e.g. Company A")]
    public string? CustomerName { get; set; }

    /// <summary>
    /// Gets or sets the address of the customer.
    /// </summary>
    [Description("Full address of the customer, e.g. 123 Main St., City, Country")]
    public InvoiceAddress? CustomerAddress { get; set; }

    /// <summary>
    /// Gets or sets the tax ID of the customer.
    /// </summary>
    [Description("Government tax ID of the customer, e.g. 123456789")]
    public string? CustomerTaxId { get; set; }

    /// <summary>
    /// Gets or sets the shipping address.
    /// </summary>
    [Description("Full address of the shipping location for the customer (null if the same as customer address), e.g. 123 Main St., City, Country")]
    public InvoiceAddress? ShippingAddress { get; set; }

    /// <summary>
    /// Gets or sets the purchase order number.
    /// </summary>
    [Description("Purchase order reference number, e.g. PO-1234")]
    public string? PurchaseOrder { get; set; }

    /// <summary>
    /// Gets or sets the invoice number.
    /// </summary>
    [Description("Reference ID for the invoice (often invoice number), e.g. INV-1234")]
    public string? InvoiceId { get; set; }

    /// <summary>
    /// Gets or sets the date of the invoice.
    /// </summary>
    [Description("Date the invoice was issued or delivered, e.g., 2021-01-01")]
    public string? InvoiceDate { get; set; }

    /// <summary>
    /// Gets or sets the due date of the invoice.
    /// </summary>
    [Description("Date when the invoice should be paid, e.g., 2021-01-15")]
    public string? PayableBy { get; set; }

    /// <summary>
    /// Gets or sets the name of the vendor.
    /// </summary>
    [Description("Name of the vendor issuing the invoice, e.g. Company B")]
    public string? VendorName { get; set; }

    /// <summary>
    /// Gets or sets the address of the vendor.
    /// </summary>
    [Description("Full address of the vendor, e.g. 123 Main St., City, Country")]
    public InvoiceAddress? VendorAddress { get; set; }

    /// <summary>
    /// Gets or sets the tax ID of the vendor.
    /// </summary>
    [Description("Government tax ID of the vendor, e.g. 123456789")]
    public string? VendorTaxId { get; set; }

    /// <summary>
    /// Gets or sets the remittance address.
    /// </summary>
    [Description("Full address for remitting payment to the vendor (null if the same as vendor address), e.g. 123 Main St., City, Country")]
    public InvoiceAddress? RemittanceAddress { get; set; }

    /// <summary>
    /// Gets or sets the subtotal amount.
    /// </summary>
    [Description("Subtotal amount before discounts and taxes, e.g. 100.00")]
    public float? Subtotal { get; set; }

    /// <summary>
    /// Gets or sets the total discount amount.
    /// </summary>
    [Description("Total discount amount applied to the invoice, e.g. 10.00")]
    public float? TotalDiscount { get; set; }

    /// <summary>
    /// Gets or sets the total tax amount.
    /// </summary>
    [Description("Total tax amount applied to the invoice, e.g. 18.00")]
    public float? TotalTax { get; set; }

    /// <summary>
    /// Gets or sets the total amount.
    /// </summary>
    [Description("Total amount due on the invoice, e.g. 108.00")]
    public float? InvoiceTotal { get; set; }

    /// <summary>
    /// Gets or sets the payment terms.
    /// </summary>
    [Description("Payment terms for the invoice, e.g. Net 30")]
    public string? PaymentTerms { get; set; }

    /// <summary>
    /// Gets or sets the line items.
    /// </summary>
    [Description("List of line items on the invoice")]
    public List<InvoiceItem>? Items { get; set; }

    /// <summary>
    /// Gets or sets the total quantity of items.
    /// </summary>
    [Description("Total quantity of line items on the invoice")]
    public float? TotalItemQuantity { get; set; }

    /// <summary>
    /// Gets or sets the customer signature.
    /// </summary>
    [Description("Signature of the customer for the line items on the invoice")]
    public InvoiceSignature? ItemsCustomerSignature { get; set; }

    /// <summary>
    /// Gets or sets the vendor signature.
    /// </summary>
    [Description("Signature of the vendor for the line items on the invoice")]
    public InvoiceSignature? ItemsVendorSignature { get; set; }

    /// <summary>
    /// Gets or sets the return items.
    /// </summary>
    [Description("List of line items being returned")]
    public List<InvoiceItem>? Returns { get; set; }

    /// <summary>
    /// Gets or sets the total quantity of return items.
    /// </summary>
    [Description("Total quantity of line items being returned")]
    public float? TotalReturnQuantity { get; set; }

    /// <summary>
    /// Gets or sets the customer signature for return items.
    /// </summary>
    [Description("Signature of the customer for the line items being returned")]
    public InvoiceSignature? ReturnsCustomerSignature { get; set; }

    /// <summary>
    /// Gets or sets the vendor signature for return items.
    /// </summary>
    [Description("Signature of the vendor for the line items being returned")]
    public InvoiceSignature? ReturnsVendorSignature { get; set; }
}
