from __future__ import annotations
from typing import Optional
from pydantic import BaseModel, Field


class InvoiceCurrency(BaseModel):
    """
    A class representing a currency in an invoice.
    """

    currency_code: Optional[str] = Field(
        description='Currency code, e.g. USD'
    )
    amount: Optional[float] = Field(
        description='Currency amount, e.g. 100.00'
    )


class InvoiceAddress(BaseModel):
    """
    A class representing an address in an invoice.
    """

    street: Optional[str] = Field(
        description='Street address, e.g. 123 456th St.'
    )
    city: Optional[str] = Field(
        description='Name of city, town, village, etc., e.g. New York'
    )
    state: Optional[str] = Field(
        description='Name of State or local administrative division, e.g. NY'
    )
    postal_code: Optional[str] = Field(
        description='Postal code, e.g. 10001'
    )
    country: Optional[str] = Field(
        description='Country, e.g. USA'
    )


class InvoiceSignature(BaseModel):
    """
    A class representing a signature in an invoice.
    """

    signatory: Optional[str] = Field(
        description='Name of the person who signed the invoice, e.g. John Doe'
    )

    date: Optional[str] = Field(
        description='Date when the invoice was signed, e.g. 2019-11-15'
    )

    has_written_signature: Optional[bool] = Field(
        description='Indicates if the invoice has a written signature, e.g. true'
    )


class InvoiceItem(BaseModel):
    """
    A class representing a line item in an invoice.
    """

    product_code: Optional[str] = Field(
        description='Product code, product number, or SKU for the line item, e.g. A123',
    )
    description: Optional[str] = Field(
        description='Text description for the line item, e.g. Consulting service',
    )
    quantity: Optional[int] = Field(
        description='Quantity for the line item, e.g. 2',
    )
    tax: Optional[InvoiceCurrency] = Field(
        description='Tax amount applied to the line item, e.g. 6.00',
    )
    unit_price: Optional[InvoiceCurrency] = Field(
        description='Net or gross price of one unit of the line item, e.g. 30.00',
    )
    total: Optional[InvoiceCurrency] = Field(
        description='Total charges for the line item, e.g. 60.00',
    )


class Invoice(BaseModel):
    """
    A class representing an invoice.
    """

    customer_name: Optional[str] = Field(
        description='Name of the customer being invoiced, e.g. Microsoft Corp'
    )
    customer_tax_id: Optional[str] = Field(
        description='Government tax ID of the customer, e.g. 765432-1'
    )
    customer_address: Optional[InvoiceAddress] = Field(
        description='Full mailing address of the customer, e.g. 123 Other St., Redmond, WA, 98052, USA'
    )
    shipping_address: Optional[InvoiceAddress] = Field(
        description='Explicit full shipping address for the customer (null if the same as customer address), e.g. 123 Ship St., Redmond, WA, 98052, USA'
    )
    purchase_order: Optional[str] = Field(
        description='Purchase order reference number, e.g. PO-3333'
    )
    invoice_id: Optional[str] = Field(
        description='Reference ID or invoice number for the invoice, e.g. INV-100'
    )
    invoice_date: Optional[str] = Field(
        description='Date the invoice was issued, e.g., 2019-11-15'
    )
    due_date: Optional[str] = Field(
        description='Date payment for the invoice is due, e.g., 2019-12-15'
    )
    vendor_name: Optional[str] = Field(
        description='Name of the vendor/supplier who created the invoice, e.g. CONTOSO LTD.'
    )
    vendor_address: Optional[InvoiceAddress] = Field(
        description='Full mailing address of the vendor/supplier, e.g. 123 456th St, New York, NY, 10001, USA'
    )
    vendor_tax_id: Optional[str] = Field(
        description='Government tax ID of the vendor/supplier, e.g. 123456-7'
    )
    remittance_address: Optional[InvoiceAddress] = Field(
        description='Explicit full remittance or payment address for where the payment should be sent (null if the same as vendor address), e.g. 123 Remit St, New York, NY, 10001, USA'
    )
    subtotal: Optional[InvoiceCurrency] = Field(
        description='Subtotal charges for the invoice before discounts and taxes, e.g. 100.00'
    )
    total_discount: Optional[InvoiceCurrency] = Field(
        description='Total discount applied to the invoice, e.g. 5.00'
    )
    total_tax: Optional[InvoiceCurrency] = Field(
        description='Total tax applied to the invoice, e.g. 5.00'
    )
    invoice_total: Optional[InvoiceCurrency] = Field(
        description='Total charges for the invoice after discounts and taxes, e.g. 100.00'
    )
    payment_term: Optional[str] = Field(
        description='Terms of payment for the invoice, e.g. Net30'
    )
    items: Optional[list[InvoiceItem]] = Field(
        description='List of line items in the invoice'
    )
    customer_signature: Optional[InvoiceSignature] = Field(
        description='Signature of the customer, e.g. John Doe'
    )
