def validatePage(pageJS: dict, data: dict = {}) -> None | dict:
    if not pageJS.get('offer'): return
    offers = data.setdefault('offers', {})
    addresses = data.setdefault('addresses', {})
    realty_inside = data.setdefault('realty_inside', {})
    realty_outside = data.setdefault('realty_outside', {})
    realty_details = data.setdefault('realty_details', {})
    offers_details = data.setdefault('offers_details', {})
    developers = data.setdefault('developers', {})

    page: dict = pageJS['offer']
    cianid = page.get('cianId')
    tables = [offers, addresses, realty_inside, realty_outside,
              realty_details, offers_details, developers]
    for d in tables: d['cian_id'] = cianid

    offers['price'] = page.get('priceTotalRur')
    if offers['cian_id'] is None or offers['price'] is None: return

    if page.get('trackingData', {}).get('oblId') != 1: return
    offers['photos_count'] = len(page['photos']) if page.get('photos') else None
    offers['floor_number'] = page.get('floorNumber')
    offers['category'] = page.get('category')
    offers['publication_at'] = page.get('publicationDate')

    offers_details['deal_type'] = page.get('dealType')
    offers_details['flat_type'] = page.get('flatType')
    offers_details['is_duplicate'] = page.get('isDuplicate')
    offers_details['description'] = page.get('description')

    realty_inside['rooms_count'] = page.get('roomsCount')
    realty_details['is_apartment'] = page.get('isApartments')
    realty_details['is_penthouse'] = page.get('isPenthouse')

    realty_inside['repair_type'] = page.get('repairType')
    realty_inside['balconies'] = page.get('balconiesCount')
    realty_inside['loggias'] = page.get('loggiasCount')
    realty_inside['separated_wc'] = page.get('separateWcsCount')
    realty_inside['combined_wc'] = page.get('combinedWcsCount')
    realty_inside['windows_view'] = page.get('windowsViewType')

    realty_details['realty_type'] = page.get('offerType')

    if building := page.get('building'):
        offers['floors_сount'] = building.get('floorsCount')
        realty_outside['garbage_chute'] = building.get('hasGarbageChute')
        realty_outside['passenger_lifts'] = building.get('passengerLiftsCount')
        realty_outside['cargo_lifts'] = building.get('cargoLiftsCount')
        realty_outside['build_year'] = building.get('buildYear')
        realty_outside['parking_type'] = building.get('parking', {}).get('type')
        condit = (realty_outside['passenger_lifts'] or 0) + \
            (realty_outside['cargo_lifts'] or 0)
        realty_inside['ceiling_height'] = float(building.get('ceilingHeight', 0)) or None
        realty_outside['lifts_count'] = condit or None

    if houseData := pageJS.get('bti', {}).get('houseData'):
        realty_details['is_emergency'] = houseData.get('isEmergency')
        realty_details['gas_type'] = houseData.get('houseGasSupplyType')
        realty_details['renovation_programm'] = houseData.get(
            'demolishedInMoscowProgramm')
        realty_details['heat_type'] = houseData.get('houseHeatSupplyType')
        realty_details['project_type'] = houseData.get('seriesName')
        realty_outside['entrances'] = houseData.get('entrances')
        realty_outside['material_type'] = houseData.get('houseMaterialType')
        if not realty_outside.get('build_year'):
            realty_outside['build_year'] = houseData.get('yearRelease')

    if priceChanges := pageJS.get('priceChanges'):
        offers['price_changes'] = priceChanges

    if bargainTerms := page.get('bargainTerms'):
        realty_details['is_mortgage_allowed'] = bargainTerms.get('mortgageAllowed')
        offers_details['sale_type'] = bargainTerms.get('saleType')

    if newbuilding := page.get('newbuilding'):
        if newhouse := newbuilding.get('house'):
            realty_details['finish_date'] = newhouse.get('finishDate')
            developers['is_reliable'] = newhouse.get('isReliable')
        realty_details['is_premium'] = newbuilding.get('isPremium')

    if company := pageJS.get('company'):
        if reviewStats := company.get('reviewStats'):
            developers['review_count'] = reviewStats.get('reviewCount')
            developers['total_rate'] = reviewStats.get('totalRate')
        developers['name'] = company.get('name')
        developers['buildings_count'] = company.get('offersCount')
        developers['foundation_year'] = company.get('yearFoundation')

    if geo := page.get('geo'):
        addresses['coordinates'] = geo.get('coordinates')

        undergrounds = geo.get('undergrounds')
        if undergrounds and (geound := undergrounds[0]):
            addresses['metro'] = geound.get('name')
            addresses['travel_type'] = geound.get('travelType')
            addresses['travel_time'] = geound.get('travelTime')

        if geoaddr := geo.get('address'):
            addresses['address'] = geoaddr
            for i in geoaddr:
                if i.get('type') == 'okrug':
                    addresses['county'] = i.get('shortName')
                elif i.get('type') == 'raion':
                    addresses['district'] = i.get('name')
                elif i.get('type') == 'street':
                    addresses['street'] = i.get('fullName')
                elif i.get('type') == 'house':
                    addresses['house'] = i.get('fullName')

    realty_inside['total_area'] = float(page.get('totalArea', 0)) or None
    realty_inside['living_area'] = float(page.get('livingArea', 0)) or None
    realty_inside['kitchen_area'] = float(page.get('kitchenArea', 0)) or None
    offers_details['agent_name'] = pageJS.get('agent', {}).get('companyName')
    offers['views_count'] = pageJS.get('stats', {}).get('total')
    return data
