$pharmaceuticalForm.on('submit', (e) => {

    e.preventDefault();

    if ($('#pharmaceuticalCompanyName').val() === '' || $('#pharmaceuticalCompanyAddress')
        .val() === '' || $(
            '#pharmaceuticalCountryOrigin')
        .val() === '' || $('#pharmaceuticalCompanyTel').val() === '' || $(
            '#pharmaceuticalCompanyFax').val() ===
        '' || $(
            '#pharmaceuticalCompanyEmail').val() === '' || $('#pharmaceuticalProdName')
        .val() === '' || $(
            '#pharmaceuticalPackSize').val() ===
        '' || $('#PharmaceuticalDosage').val() === '' || $('#RouteOfAdministration').val() ===
        '' || $(
            '#mainIndication')
        .val() === '' || $('#descriptionOfProduct').val() === '' || $('#shelfLifeAfterDilution')
        .val() ===
        '' || $(
            '#shelfLifeAfterFirstOpening').val() === '' || $('#storageConditions').val() ===
        '' || $(
            '#storageAfterOpening').val() ===
        '' || $('#PharmacotherapeuticGroup').val() === '' || $('#ATCCode').val() === '' || $(
            '#CountryOfOrigin')
        .val() === '' || $('#CountryOfRelease').val() === '' || $('#signatoryName').val() ===
        '' ||
        $(
            '#signatoryPosition').val() === '') {
        alert('Please fill in all required fields.');
        return false;
    }

    $spinner.show();
    $pharmaceuticalForm.hide();

    $.ajax({

        type: 'POST',
        url: "/VeterinaryPharmaceutical/" + headerCode,
        data: {
            companyName: $('#pharmaceuticalCompanyName').val(),
            companyAddress: $('#pharmaceuticalCompanyAddress').val(),
            CountryOrigin: $('#pharmaceuticalCountryOrigin').val(),
            companyTel: $('#pharmaceuticalCompanyTel').val(),
            companyFax: $('#pharmaceuticalCompanyFax').val(),
            companyEmail: $('#pharmaceuticalCompanyEmail').val(),
            prodName: $('#pharmaceuticalProdName').val(),
            packSize: $('#pharmaceuticalPackSize').val(),
            PharmaceuticalDosage: $('#PharmaceuticalDosage').val(),
            RouteOfAdministration: $('#RouteOfAdministration').val(),
            mainIndication: $('#mainIndication').val(),
            descriptionOfProduct: $('#descriptionOfProduct').val(),
            shelfLifeAfterDilution: $('#shelfLifeAfterDilution').val(),
            shelfLifeAfterFirstOpening: $('#shelfLifeAfterFirstOpening').val(),
            storageConditions: $('#storageConditions').val(),
            storageAfterOpening: $('#storageAfterOpening').val(),
            PharmacotherapeuticGroup: $('#PharmacotherapeuticGroup').val(),
            ATCCode: $('#ATCCode').val(),
            CountryOfOrigin: $('#CountryOfOrigin').val(),
            CountryOfRelease: $('#CountryOfRelease').val(),
            controlledVeterinaryMedicine: $('#legal2').val(),
            prescriptionOnlyMedicine: $('#legal3').val(),
            nonPharmacy: $('#legal4').val(),
            pharmaciesOnly: $('#legal5').val(),
            signatoryName: $('#signatoryName').val(),
            signatoryPosition: $('#signatoryPosition').val(),
            iAgree: $('#iAgree').val(),
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
        },

        success: function (response) {
            $spinner.hide();

            if (response['success'] === true) {

                iziToast.show({
                    theme: 'dark',
                    backgroundColor: '#239B56',
                    icon: 'las la-check-circle',
                    title: 'Yeah',
                    message: response['response'],
                    position: 'topRight',
                    progressBarColor: '#F4F6F7',

                });
                $step2Icon.addClass('completed');
                $stepTwo.hide();
                $stepThree.show();
                $('#pharmaceuticalCompanyName, #pharmaceuticalCompanyAddress, #pharmaceuticalCountryOrigin')
                    .val('');
                $('#pharmaceuticalCompanyTel, #pharmaceuticalCompanyFax, #pharmaceuticalCompanyEmail')
                    .val('');
                $('#pharmaceuticalProdName, #pharmaceuticalPackSize, #PharmaceuticalDosage, #RouteOfAdministration')
                    .val('');
                $('#mainIndication, #descriptionOfProduct, #shelfLifeAfterDilution, #shelfLifeAfterFirstOpening')
                    .val('');
                $('#storageConditions, #PharmacotherapeuticGroup, #ATCCode, #CountryOfOrigin, #CountryOfRelease')
                    .val('');
                $('#legal2, #legal3, #legal4, #legal5, #signatoryName, #signatoryPosition')
                    .val('');
            } else if (response['error']) {

                iziToast.show({
                    theme: 'dark',
                    icon: 'las la-exclamation',
                    title: 'Error',
                    message: response['error'],
                    position: 'topRight',
                    progressBarColor: '#ff0800',
                });
                $pharmaceuticalForm.show();
            }
        },

        error: function (error) {
            console.log(error)
            $spinner.hide();
            $pharmaceuticalForm.show();
        }
    });

});


$ingredientForm.on('submit', (e) => {

    e.preventDefault();
    if ($('#ingredientType').val() === '' || $('#ingredientName')
        .val() === '' || $(
            '#quantityPerDose')
        .val() === '' || $('#strengthOfIngredient').val() === '' || $(
            '#Proportion').val() ===
        '' || $(
            '#specification').val() === '') {
        alert('Please fill in all required fields.');
        return false;
    }
    $spinner.show();
    $.ajax({

        type: 'POST',
        url: "/active/ingredients/" + headerCode,
        data: {
            myAction: $('#ingredientMyAction').val(),
            lineNo: $('#ingredientlineNo').val(),
            ingredientType: $('#ingredientType').val(),
            ingredientName: $('#ingredientName').val(),
            quantityPerDose: $('#quantityPerDose').val(),
            strengthOfIngredient: $('#strengthOfIngredient').val(),
            Proportion: $('#Proportion').val(),
            ReasonForInclusion: $('#ReasonForInclusion').val(),
            specification: $('#specification').val(),
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
        },

        success: function (response) {
            $spinner.hide();

            if (response['success'] === true) {

                iziToast.show({
                    theme: 'dark',
                    backgroundColor: '#239B56',
                    icon: 'las la-check-circle',
                    title: 'Yeah',
                    message: response['response'],
                    position: 'topRight',
                    progressBarColor: '#F4F6F7',

                });
                $step2Icon.addClass('completed');
                loadIngredients(headerCode);
                $('#ingredientType, #ingredientName, #quantityPerDose')
                    .val('');
                $('#strengthOfIngredient, #Proportion, #ReasonForInclusion')
                    .val('');
                $('#specification')
                    .val('');
            } else if (response['error']) {

                iziToast.show({
                    theme: 'dark',
                    icon: 'las la-exclamation',
                    title: 'Error',
                    message: response['error'],
                    position: 'topRight',
                    progressBarColor: '#ff0800',
                });
            }
        },

        error: function (error) {
            console.log(error)
            $spinner.hide();
        }
    });

});

$ManufacturerForm.on('submit', (e) => {

    e.preventDefault();
    if ($('#TypeOfManufacturer').val() === '' || $('#manufacturerName')
        .val() === '' || $(
            '#plantAddress')
        .val() === '' || $('#manufacturer_country').val() === '' || $(
            '#ManufacturerTelephone').val() ===
        '' || $(
            '#ManufacturerEmail').val() === '' || $(
            '#ManufacturerGMP').val() === '' || $(
            '#manufacturer_activity').val() === '') {
        alert('Please fill in all required fields.');
        return false;
    }
    $spinner.show();
    $.ajax({

        type: 'POST',
        url: "/manufacturer/particulars/" + headerCode,
        data: {
            myAction: $('#Manufacturer_myAction').val(),
            lineNo: $('#Manufacturer_lineNo').val(),
            TypeOfManufacturer: $('#TypeOfManufacturer').val(),
            manufacturerOther: $('#manufacturerOther').val(),
            manufacturerName: $('#manufacturerName').val(),
            plantAddress: $('#plantAddress').val(),
            country: $('#manufacturer_country').val(),
            ManufacturerTelephone: $('#ManufacturerTelephone').val(),
            ManufacturerEmail: $('#ManufacturerEmail').val(),
            ManufacturerGMP: $('#ManufacturerGMP').val(),
            activity: $('#manufacturer_activity').val(),
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
        },

        success: function (response) {
            $spinner.hide();

            if (response['success'] === true) {

                iziToast.show({
                    theme: 'dark',
                    backgroundColor: '#239B56',
                    icon: 'las la-check-circle',
                    title: 'Yeah',
                    message: response['response'],
                    position: 'topRight',
                    progressBarColor: '#F4F6F7',

                });
                loadManufacturer(headerCode);
                $step4Icon.addClass('completed');
                $('#TypeOfManufacturer, #manufacturerName, #plantAddress')
                    .val('');
                $('#manufacturer_country, #ManufacturerTelephone, #ManufacturerEmail')
                    .val('');
                $('#ManufacturerGMP, #manufacturer_activity')
                    .val('');
            } else if (response['error']) {

                iziToast.show({
                    theme: 'dark',
                    icon: 'las la-exclamation',
                    title: 'Error',
                    message: response['error'],
                    position: 'topRight',
                    progressBarColor: '#ff0800',
                });
            }
        },

        error: function (error) {
            console.log(error)
            $spinner.hide();
        }
    });

});
$MarketingForm.on('submit', (e) => {

    e.preventDefault();
    if ($('#AuthorisationStatus').val() === '') {
        alert('Please fill in all required fields.');
        return false;
    }
    $spinner.show();
    $.ajax({
        type: 'POST',
        url: "/marketing/authorization/" + headerCode,
        data: {
            myAction: $('#market_myAction').val(),
            lineNo: $('#market_lineNo').val(),
            AuthorisationStatus: $('#AuthorisationStatus').val(),
            MarketingCountry: $('#MarketingCountry').val(),
            DateAuthorisation: $('#DateAuthorisation').val(),
            ProprietaryName: $('#ProprietaryName').val(),
            AuthorisationNumber: $('#AuthorisationNumber').val(),
            AuthorisationReason: $('#AuthorisationReason').val(),
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
        },

        success: function (response) {
            $spinner.hide();
            if (response['success'] === true) {
                iziToast.show({
                    theme: 'dark',
                    backgroundColor: '#239B56',
                    icon: 'las la-check-circle',
                    title: 'Yeah',
                    message: response['response'],
                    position: 'topRight',
                    progressBarColor: '#F4F6F7',

                });
                loadMarketing(headerCode);
                $('#AuthorisationStatus, #MarketingCountry, #DateAuthorisation')
                    .val('');
                $('#ProprietaryName, #AuthorisationNumber, #AuthorisationReason')
                    .val('');

            } else if (response['error']) {
                iziToast.show({
                    theme: 'dark',
                    icon: 'las la-exclamation',
                    title: 'Error',
                    message: response['error'],
                    position: 'topRight',
                    progressBarColor: '#ff0800',
                });
            }
        },

        error: function (error) {
            console.log(error)
            $spinner.hide();
        }
    });

});