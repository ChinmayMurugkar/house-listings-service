import csv
from datetime import datetime
from decimal import Decimal
from django.core.management.base import BaseCommand, CommandError
from api.models import House

class Command(BaseCommand):
    help = 'Imports house data from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file containing house data')

    def clean_price(self, price_str):
        """Clean price string by removing $, K, M and converting to decimal."""
        if not price_str or price_str.strip() == '':
            return None
        
        # Remove $ and whitespace
        price_str = price_str.strip().replace('$', '').replace(',', '')
        
        # Handle K (thousands) and M (millions)
        multiplier = 1
        if price_str.endswith('K'):
            multiplier = 1000
            price_str = price_str[:-1]
        elif price_str.endswith('M'):
            multiplier = 1000000
            price_str = price_str[:-1]
        
        try:
            return Decimal(price_str) * multiplier
        except (ValueError, TypeError):
            return None

    def clean_date(self, date_str):
        """Convert date string to datetime object."""
        if not date_str or date_str.strip() == '':
            return None
        try:
            return datetime.strptime(date_str.strip(), '%m/%d/%Y').date()
        except (ValueError, TypeError):
            return None

    def clean_int(self, value):
        """Convert string to integer, handling empty values."""
        if not value or value.strip() == '':
            return None
        try:
            return int(float(value))
        except (ValueError, TypeError):
            return None

    def clean_float(self, value):
        """Convert string to float, handling empty values."""
        if not value or value.strip() == '':
            return None
        try:
            return float(value)
        except (ValueError, TypeError):
            return None

    def clean_string(self, value):
        """Clean string values by stripping whitespace and handling empty values."""
        if not value:
            return None
        cleaned = value.strip()
        return cleaned if cleaned else None

    def handle(self, *args, **options):
        csv_file = options['csv_file']
        
        try:
            with open(csv_file, 'r') as file:
                # Read all lines and strip leading/trailing whitespace
                lines = [line.strip() for line in file.readlines()]
                
                # Get the header line and clean column names
                header = lines[0]
                fieldnames = [name.strip() for name in header.split(',')]
                
                # Create CSV reader with cleaned data
                reader = csv.DictReader(lines[1:], fieldnames=fieldnames)
                
                houses_created = 0
                houses_skipped = 0
                
                for row in reader:
                    try:
                        # Clean and convert data
                        price = self.clean_price(row['price'])
                        last_sold_price = self.clean_price(row['last_sold_price'])
                        rent_price = self.clean_price(row['rent_price'])
                        rentzestimate_amount = self.clean_price(row['rentzestimate_amount'])
                        tax_value = self.clean_price(row['tax_value'])
                        zestimate_amount = self.clean_price(row['zestimate_amount'])
                        
                        last_sold_date = self.clean_date(row['last_sold_date'])
                        rentzestimate_last_updated = self.clean_date(row['rentzestimate_last_updated'])
                        zestimate_last_updated = self.clean_date(row['zestimate_last_updated'])
                        
                        bathrooms = self.clean_float(row['bathrooms'])
                        bedrooms = self.clean_int(row['bedrooms'])
                        home_size = self.clean_int(row['home_size'])
                        property_size = self.clean_int(row['property_size'])
                        tax_year = self.clean_int(row['tax_year'])
                        year_built = self.clean_int(row['year_built'])

                        # Clean string fields
                        area_unit = self.clean_string(row['area_unit'])
                        home_type = self.clean_string(row['home_type'])
                        link = self.clean_string(row['link'])
                        zillow_id = self.clean_string(row['zillow_id'])
                        address = self.clean_string(row['address'])
                        city = self.clean_string(row['city'])
                        state = self.clean_string(row['state'])
                        zipcode = self.clean_string(row['zipcode'])

                        # Create house instance
                        house = House(
                            area_unit=area_unit or 'SqFt',  # Default to SqFt if empty
                            bathrooms=bathrooms,
                            bedrooms=bedrooms,
                            home_size=home_size,
                            home_type=home_type,
                            last_sold_date=last_sold_date,
                            last_sold_price=last_sold_price,
                            link=link,
                            price=price,
                            property_size=property_size,
                            rent_price=rent_price,
                            rentzestimate_amount=rentzestimate_amount,
                            rentzestimate_last_updated=rentzestimate_last_updated,
                            tax_value=tax_value,
                            tax_year=tax_year,
                            year_built=year_built,
                            zestimate_amount=zestimate_amount,
                            zestimate_last_updated=zestimate_last_updated,
                            zillow_id=zillow_id,
                            address=address,
                            city=city,
                            state=state,
                            zipcode=zipcode
                        )
                        
                        house.save()
                        houses_created += 1
                        
                    except Exception as e:
                        self.stdout.write(self.style.WARNING(
                            f"Error processing row: {row.get('zillow_id', 'unknown')} - {str(e)}"
                        ))
                        houses_skipped += 1
                        continue

                self.stdout.write(self.style.SUCCESS(
                    f'Successfully imported {houses_created} houses. Skipped {houses_skipped} houses.'
                ))

        except FileNotFoundError:
            raise CommandError(f'CSV file not found: {csv_file}')
        except Exception as e:
            raise CommandError(f'Error reading CSV file: {str(e)}') 