from django.contrib import admin
from django.utils.html import format_html
from django.contrib import admin

from .models import Contact


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    # Display columns in list view
    list_display = ('id', 'name', 'email', 'phone', 'listing', 'contact_date', 'user_details')
    list_display_links = ('id', 'name')

    # Filter options
    list_filter = ('contact_date', 'listing', 'user_id')

    # Search fields
    search_fields = ('name', 'email', 'phone', 'listing', 'message')

    # Pagination
    list_per_page = 20

    # Order by latest first
    ordering = ['-contact_date', '-id']

    # Read-only fields - prevent admin from modifying user submissions
    readonly_fields = ('listing', 'listing_id', 'name', 'email', 'phone', 'message',
                      'contact_date', 'user_id', 'show_booking_details')

    # Fieldsets for better organization with yellow title
    fieldsets = (
        ('<span style="color: #FFD700;">Customer Information</span>', {
            'fields': ('name', 'email', 'phone', 'user_id'),
            'classes': ('wide',),
        }),
        ('<span style="color: #FFD700;">Car Booking Details</span>', {
            'fields': ('listing', 'listing_id', 'contact_date'),
            'classes': ('wide',),
        }),
        ('<span style="color: #FFD700;">Message & Additional Info</span>', {
            'fields': ('message',),
            'classes': ('wide',),
        }),
        ('<span style="color: #FFD700;">Booking Summary</span>', {
            'fields': ('show_booking_details',),
            'classes': ('wide',),
            'description': 'Complete booking details at a glance'
        }),
    )

    def user_details(self, obj):
        """Show user details in list view"""
        if obj.user_id and obj.user_id != 0:
            return format_html(
                '<span style="color: green;">✓ Registered User (ID: {})</span>',
                obj.user_id
            )
        else:
            return format_html(
                '<span style="color: orange;">○ Guest User</span>'
            )
    user_details.short_description = '<span style="color: #FFD700;">User Type</span>'

    def show_booking_details(self, obj):
        """Display complete booking details in a nice format"""
        user_type = "Registered User" if obj.user_id and obj.user_id != 0 else "Guest User"

        details = f"""
        <div style="padding: 15px; border: 1px solid #ddd; border-radius: 5px; background-color: #f9f9f9;">
            <h3 style="color: #FFD700; margin-top: 0;">📅 Test Drive Booking Details</h3>

            <table style="width: 100%; border-collapse: collapse;">
                <tr style="border-bottom: 1px solid #ddd;">
                    <td style="padding: 8px; font-weight: bold; width: 30%; color: #FFD700;">Customer Name:</td>
                    <td style="padding: 8px;">{obj.name}</td>
                </tr>
                <tr style="border-bottom: 1px solid #ddd;">
                    <td style="padding: 8px; font-weight: bold; color: #FFD700;">Email:</td>
                    <td style="padding: 8px;"><a href="mailto:{obj.email}">{obj.email}</a></td>
                </tr>
                <tr style="border-bottom: 1px solid #ddd;">
                    <td style="padding: 8px; font-weight: bold; color: #FFD700;">Phone:</td>
                    <td style="padding: 8px;">{obj.phone if obj.phone else 'Not provided'}</td>
                </tr>
                <tr style="border-bottom: 1px solid #ddd;">
                    <td style="padding: 8px; font-weight: bold; color: #FFD700;">User Type:</td>
                    <td style="padding: 8px;">{user_type} (ID: {obj.user_id if obj.user_id else 'N/A'})</td>
                </tr>
                <tr style="border-bottom: 1px solid #ddd;">
                    <td style="padding: 8px; font-weight: bold; color: #FFD700;">Car:</td>
                    <td style="padding: 8px;">{obj.listing}</td>
                </tr>
                <tr style="border-bottom: 1px solid #ddd;">
                    <td style="padding: 8px; font-weight: bold; color: #FFD700;">Listing ID:</td>
                    <td style="padding: 8px;">{obj.listing_id}</td>
                </tr>
                <tr style="border-bottom: 1px solid #ddd;">
                    <td style="padding: 8px; font-weight: bold; color: #FFD700;">Booking Date:</td>
                    <td style="padding: 8px;">{obj.contact_date}</td>
                </tr>
                <tr>
                    <td style="padding: 8px; font-weight: bold; color: #FFD700; vertical-align: top;">Message:</td>
                    <td style="padding: 8px;">{obj.message if obj.message else 'No message provided'}</td>
                </tr>
            </table>

            <div style="margin-top: 15px; padding: 10px; background-color: #e7f3ff; border-radius: 3px; border: 2px solid #FFD700;">
                <strong style="color: #FFD700;">📧 Email sent to: {obj.email}</strong><br>
                <strong style="color: #FFD700;">📧 Admin notified at: boy749377@gmail.com</strong>
            </div>
        </div>
        """
        return format_html(details)

    show_booking_details.short_description = '<span style="color: #FFD700;">Booking Summary</span>'

    def has_add_permission(self, request):
        """Disable adding contacts manually through admin"""
        return False

    def has_change_permission(self, request, obj=None):
        """Make all fields read-only"""
        return True

    class Media:
        css = {
            'all': ('admin/css/custom_admin.css',)
        }
        js = ('admin/js/custom_admin.js',)
