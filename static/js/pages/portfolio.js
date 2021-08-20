$(document).ready(function(){
    const versionMax = 1;
    var version = versionMax;
    var portfolioName = 'InitialPortfolio';

    setVersion(version);

    loadPortfolio(version, portfolioName);

    rightVersionArrow = $('#right-version-arrow');
    leftVersionArrow = $('#left-version-arrow');

    rightVersionArrow.click(function(){
        leftVersionArrow.hide();
        rightVersionArrow.hide();
        version+=1;
        loadPortfolio(version, portfolioName);
        addCompanyExpand();
    })

    leftVersionArrow.click(function(){
        leftVersionArrow.hide();
        rightVersionArrow.hide();
        version-=1;  
        loadPortfolio(version, portfolioName); 
        addCompanyExpand();
       });

    addCompanyExpand();
    
});


// ------- MAIN PORTFOLIO FUNCTIONS ---------- //

function addCompanyExpand(){
    $('.company-expand').each(function(index){
        expandCompanyPerformanceData(index);
        $('.company-expand').eq(index).click(function(){
            expandCompanyPerformanceData(index);
        })
    });
}

function loadPortfolio(version, portfolio_name){
    clearPortfolio();
    structurePortfolioHTML(25)
    currentPortfolio = getPortfolio(version, portfolio_name);
    
}

function loadPortfolioPerformance(name, version, date){ 
    
    $('#loading-portfolio-performance').show()
    $('#portfolio-performance-3m').text(function(){return ''});
    $('#portfolio-performance-6m').text(function(){return ''});
    $('#portfolio-performance-1y').text(function(){return ''});
    $('#portfolio-performance-5y').text(function(){return ''});
    
    $('#portfolio-performance-date').text(function(){return date});

    $.ajax({
        url: '/api/portfolio-performance',
        type: 'GET',
        data: {'name': name, 'version': version, 'date': date},
        async: true,
        dataType: 'JSON',
        success: function(data){
            $('#portfolio-performance-3m').text(function(){return data['3m']});
            $('#portfolio-performance-6m').text(function(){return data['6m']});
            $('#portfolio-performance-1y').text(function(){return data['1y']});
            $('#portfolio-performance-5y').text(function(){return data['5y']});
            $('#loading-portfolio-performance').hide()
        },
        error: function(){
            console.error('portfolio performace API called failed')
        }
    })
    
}

function loadCompanyData(ticker, index, date){

    $.ajax({
        url: '/api/portfolio-company',
        type: 'GET',
        data: {'ticker': ticker},
        async: true,
        dataType: 'JSON',
        success: function(data){
           
            // Do stuff here

            $('.company-ticker').eq(index).text(function(){return ticker});
            $('.company-full-name').eq(index).text(function(){return data['fullName']});
            $('.company-rating').eq(index).text(function(){return data['rating'].toFixed(2)});
            $('.company-rating-date').eq(index).text(function(){return data['dateRated']});

        },
        error: function(){
            console.error('Company API called failed')
        }
    });

}

function setVersion(version){
    versionMax = 1
    rightVersionArrow = $('#right-version-arrow');
    leftVersionArrow = $('#left-version-arrow');

    if(version == 1){
        leftVersionArrow.hide();
        rightVersionArrow.show();
    }

    if(version > 1 && version < versionMax){
        leftVersionArrow.show();
        rightVersionArrow.show();
    }
 
    if(version == versionMax){
        leftVersionArrow.show();
        rightVersionArrow.hide();
    }

    if(versionMax == 1){
        leftVersionArrow.hide();
        rightVersionArrow.hide();
    }

    $('#portfolio-version').text(function(){return version});
}

function structurePortfolioHTML(n){
    for(var i=0; i < n; i++){
        appendCompanySpot()
    }
}

function loadPerformanceData(ticker, date, index){
    $.ajax({
        url: '/api/company-performance',
        type: 'GET',
        data: {'ticker': ticker, 'date': date},
        async: true,
        dataType: 'JSON',
        success: function(data){

            $('.company-price').eq(index).text(function(){return data['current'].toFixed(2)});
            $('.company-performance-3m').eq(index).text(function(){return performance(data['3m'], data['current'])});
            $('.company-performance-6m').eq(index).text(function(){return performance(data['6m'], data['current'])});
            $('.company-performance-1y').eq(index).text(function(){return performance(data['1y'], data['current'])});
            $('.company-performance-5y').eq(index).text(function(){return performance(data['5y'], data['current'])});
            $('.company-performance-since-rating').eq(index).text(function(){return performance(data['rated'], data['current'])});
            $('.company-performance-date').eq(index).text(function(){return date});
        },
        error: function(data){
            console.error(data)
        }
    })
}

function performance(entry, exit){
    return ((exit-entry)/entry * 100).toFixed(2);
}

// ------- HELPER FUNCTIONS ---------- //


function appendCompanySpot(){

    var htmlString = '<div class="cell small-10 small-offset-1 medium-8 medium-offset-2 large-4 large-offset-1 portfolio__performance-table portfolio-item margin-bottom-100"><h2><span class="company-ticker"></span> <small><span class="company-full-name"></span></small></h2><p>Aliias rated <span class="company-rating"></span> on <span class="company-rating-date"></span>.</p><div class="grid-x company-performance-stats"><div class="cell medium-4"><h4>Price</h4><p>$<span class="company-price"></span></p></div><div class="cell medium-4 "><h4>3 Month</h4><p><span class="company-performance-3m"></span> %</p></div><div class="cell medium-4"><h4>6 Month</h4><p><span class="company-performance-6m"></span> %</p></div><div class="cell medium-4"><h4>1 Year</h4><p><span class="company-performance-1y"></span> %</p></div><div class="cell medium-4"><h4>5 Year</h4><p><span class="company-performance-5y"></span> %</p></div><div class="cell medium-4"><h4>Since Rating</h4><p><span class="company-performance-since-rating"></span> %</p></div></div><br><p>As of <span class="company-performance-date"></span><span class="company-expand material-icons float-right">expand_less</span></p><hr></div>'

    $('#portfolio').append(htmlString)

}

function clearPortfolio(){
    $('.portfolio-item ').remove();
}

function getPortfolio(version, name){

    var portfolio = {}

    $.ajax({
        url: '/api/get-portfolio',
        type: 'GET',
        data: {'version': version, 'name': name},
        async: true,
        dataType: 'JSON',
        success: function(data){
            

            portfolio['tickers'] = data['tickers'];
                        
            $('#portfolio-creation-date').text(function(){return data['date_created']});
            
            currentDate = today()

            loadPortfolioPerformance(name, version, currentDate)

            portfolio['tickers'].forEach(function(ticker, index){
                loadCompanyData(ticker,index);
                loadPerformanceData(ticker, currentDate, index);
            });

            setVersion(version);

            
        },
        error: function(){
            console.error('Portfolio API called failed')
        }
    });
}

function expandCompanyPerformanceData(index){
    var expandButton = $('.company-expand').eq(index);
    if(expandButton.text() == 'expand_less'){
        // close
        $('.company-performance-stats').eq(index).hide();
        expandButton.text(function(){return 'expand_more'});
    }else{
        // expand
        $('.company-performance-stats').eq(index).show();
        expandButton.text(function(){return 'expand_less'});
    }
}

function today(){
    var today = new Date();
    var dd = String(today.getDate()).padStart(2, '0');
    var mm = String(today.getMonth() + 1).padStart(2, '0'); //January is 0!
    var yyyy = today.getFullYear();

    today = yyyy + '-' + mm + '-' + dd;
    return today
}



