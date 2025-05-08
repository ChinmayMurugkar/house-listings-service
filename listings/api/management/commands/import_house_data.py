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

    def handle(self, *args, **options):
        csv_file = options['csv_file']
        
        try:
            with open(csv_file, 'r') as file:
                reader = csv.DictReader(file)
                houses_created = 0
                houses_skipped = 0
                
                for row in reader:
                    try:
                        # Clean and convert data
                        price = self.clean_price(row.get('price', ''))
                        last_sold_price = self.clean_price(row.get('last_sold_price', ''))
                        rent_price = self.clean_price(row.get('rent_price', ''))
                        rentzestimate_amount = self.clean_price(row.get('rentzestimate_amount', ''))
                        tax_value = self.clean_price(row.get('tax_value', ''))
                        zestimate_amount = self.clean_price(row.get('zestimate_amount', ''))
                        
                        last_sold_date = self.clean_date(row.get('last_sold_date', ''))
                        rentzestimate_last_updated = self.clean_date(row.get('rentzestimate_last_updated', ''))
                        zestimate_last_updated = self.clean_date(row.get('zestimate_last_updated', ''))
                        
                        bathrooms = self.clean_float(row.get('bathrooms', ''))
                        bedrooms = self.clean_int(row.get('bedrooms', ''))
                        home_size = self.clean_int(row.get('home_size', ''))
                        property_size = self.clean_int(row.get('property_size', ''))
                        tax_year = self.clean_int(row.get('tax_year', ''))
                        year_built = self.clean_int(row.get('year_built', ''))

                        # Create house instance
                        house = House(
                            area_unit=row.get('area_unit', ''),
                            bathrooms=bathrooms,
                            bedrooms=bedrooms,
                            home_size=home_size,
                            home_type=row.get('home_type', ''),
                            last_sold_date=last_sold_date,
                            last_sold_price=last_sold_price,
                            link=row.get('link', ''),
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
                            zillow_id=row.get('zillow_id', ''),
                            address=row.get('address', ''),
                            city=row.get('city', ''),
                            state=row.get('state', ''),
                            zipcode=row.get('zipcode', '')
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
