import check_ps_codes

valid_codes = check_ps_codes.valid_codes
country_map = {}
for code in valid_codes:
    # Extract country part (last two letters after last '-')
    country = code.split('-')[-1]
    # Prefer English if available
    if country not in country_map or (code.startswith('en-') and not country_map[country].startswith('en-')):
        country_map[country] = code

unique_codes = sorted(country_map.values())

print(unique_codes)
print(len(unique_codes))
