# Calculator definitions for 67858.com. Each entry renders to /calculators/<slug>.html
# inputs: (key, label, default, prefix, suffix, step, hint)  prefix 'cur' = currency symbol
# select inputs: (key, label, default, 'select', [(value,label),...], None, hint)

CATS = {
    "money": ("Money & Loans", "💰", "Loans, mortgages, interest, savings and debt — the decisions that cost or earn you the most."),
    "business": ("Business & Pricing", "📈", "Margins, break-even, ROI, unit economics and runway for founders and small businesses."),
    "web-ai": ("Websites, Creators & AI", "🤖", "Ad revenue, site valuation, domain flips, AI costs and creator earnings."),
    "everyday": ("Everyday Numbers", "🔢", "Percentages, discounts, tips, taxes and price comparisons — fast answers."),
}

C = []
def add(**k): C.append(k)

add(slug="loan-emi-calculator", cat="money", icon="🏦", title="Loan EMI Calculator",
    short="Monthly payment, total interest and yearly breakdown for any fixed-rate loan.",
    inputs=[("P","Loan amount",25000,"cur","",100,"Amount borrowed"),("r","Annual interest rate",9,"","%",0.05,"Nominal APR"),("y","Loan term",5,"","years",1,"")],
    js="""var i=v.r/1200,n=Math.round(v.y*12),P=v.P,e=i?P*i*Math.pow(1+i,n)/(Math.pow(1+i,n)-1):P/n;
var bal=P,data=[],yp=0,yi=0;for(var m=1;m<=n;m++){var it=bal*i,pr=e-it;bal-=pr;yp+=pr;yi+=it;if(m%12===0||m===n){data.push({l:'Y'+Math.ceil(m/12),a:yp,b:yi});yp=0;yi=0}}
return {results:[{l:'Monthly payment (EMI)',v:e,f:'money'},{l:'Total interest',v:e*n-P,f:'money'},{l:'Total repaid',v:e*n,f:'money'},{l:'Number of payments',v:n,f:'int'}],
series:{a:'Principal',b:'Interest',data:data},steps:'EMI = P × i × (1+i)<sup>n</sup> ÷ ((1+i)<sup>n</sup> − 1), with i = '+(i*100).toFixed(4)+'% per month and n = '+n+'.'};""",
    formula="EMI = P × i × (1 + i)^n ÷ ((1 + i)^n − 1)\n  P = principal, i = annual rate ÷ 12, n = months",
    intro="An EMI (equated monthly instalment) is the fixed payment that clears a loan — interest and principal — over its term. Early payments are mostly interest; later ones are mostly principal. The yearly chart shows that shift so you can see when extra payments save the most.",
    example="Borrow 25,000 at 9% for 5 years: i = 0.0075 and n = 60, so the EMI is about 518.96. Over 60 payments you repay about 31,137.53, meaning roughly 6,137.53 is interest.",
    faqs=[("Does a longer term lower the cost?","It lowers the monthly payment but raises total interest, because the balance stays outstanding longer."),("Is this the same as APR?","This tool uses the nominal annual rate. APR may also include fees, which raises the true cost — add fees to the loan amount for a closer estimate."),("Do prepayments help?","Yes. Extra principal early in the loan removes future interest on that amount for every remaining month.")])

add(slug="mortgage-calculator", cat="money", icon="🏠", title="Mortgage Calculator",
    short="Full monthly housing cost: principal & interest, property tax, insurance and HOA.",
    inputs=[("price","Home price",400000,"cur","",1000,""),("down","Down payment",20,"","%",0.5,""),("r","Interest rate",6.5,"","%",0.05,""),("y","Term",30,"","years",1,""),("tax","Property tax / year",4800,"cur","",50,""),("ins","Home insurance / year",1500,"cur","",50,""),("hoa","HOA / month",0,"cur","",10,"")],
    js="""var L=v.price*(1-v.down/100),i=v.r/1200,n=v.y*12,pi=i?L*i*Math.pow(1+i,n)/(Math.pow(1+i,n)-1):L/n,t=pi+v.tax/12+v.ins/12+v.hoa;
var bal=L,data=[],yp=0,yi=0;for(var m=1;m<=n;m++){var it=bal*i,pr=pi-it;bal-=pr;yp+=pr;yi+=it;if(m%12===0){if((m/12)%Math.max(1,Math.round(v.y/15))===0)data.push({l:'Y'+m/12,a:yp,b:yi});yp=0;yi=0}}
return {results:[{l:'Total monthly payment',v:t,f:'money'},{l:'Principal & interest',v:pi,f:'money'},{l:'Loan amount',v:L,f:'money0'},{l:'Total interest over term',v:pi*n-L,f:'money0'},{l:'Down payment',v:v.price*v.down/100,f:'money0'}],series:{a:'Principal',b:'Interest',data:data}};""",
    formula="Loan = Price × (1 − Down%)\nP&I = Loan × i × (1+i)^n ÷ ((1+i)^n − 1)\nMonthly total = P&I + Tax/12 + Insurance/12 + HOA",
    intro="Lenders approve you on the full monthly cost, not just principal and interest. This calculator adds property tax, insurance and HOA so the number you see is the number that leaves your account.",
    example="A 400,000 home with 20% down leaves a 320,000 loan. At 6.5% over 30 years, principal and interest is about 2,022.62 per month; adding 400 tax, 125 insurance gives roughly 2,547.62.",
    faqs=[("What down payment avoids mortgage insurance?","Many conventional lenders require private mortgage insurance below 20% down. Rules vary by country and lender."),("Should I pick 15 or 30 years?","A 15-year loan has a higher payment but far less total interest; a 30-year loan keeps cash flow flexible."),("Are taxes and insurance fixed?","No. Both usually rise over time, so treat the totals as today's estimate.")])

add(slug="compound-interest-calculator", cat="money", icon="📊", title="Compound Interest Calculator",
    short="Grow a lump sum plus monthly contributions with any compounding frequency.",
    inputs=[("P","Starting amount",10000,"cur","",100,""),("c","Monthly contribution",300,"cur","",10,""),("r","Annual return",7,"","%",0.1,""),("y","Years",30,"","years",1,""),("k","Compounding","12","select",[("1","Annually"),("4","Quarterly"),("12","Monthly"),("365","Daily")],None,"")],
    js="""var k=+v.k,m=Math.pow(1+v.r/100/k,k/12)-1,b=v.P,dep=v.P,data=[];
for(var mo=1;mo<=v.y*12;mo++){b=b*(1+m)+v.c;dep+=v.c;if(mo%12===0&&((mo/12)%Math.max(1,Math.round(v.y/15))===0))data.push({l:'Y'+mo/12,a:dep,b:Math.max(0,b-dep)})}
return {results:[{l:'Future value',v:b,f:'money'},{l:'Total contributed',v:dep,f:'money'},{l:'Interest earned',v:b-dep,f:'money'},{l:'Growth multiple',v:dep?b/dep:0,f:'x'}],series:{a:'Contributions',b:'Growth',data:data},steps:'Rule of 72: money doubles roughly every '+(v.r?(72/v.r).toFixed(1):'∞')+' years at '+v.r+'%.'};""",
    formula="A = P(1 + r/k)^(k·t)   (lump sum)\nContributions are added monthly and grown at the equivalent monthly rate.",
    intro="Compound interest pays returns on previous returns. Time is the dominant input — the chart's gold segment (growth) eventually dwarfs the teal segment (your deposits).",
    example="10,000 at 7% compounded annually for 30 years becomes about 76,122.55. Compounded monthly it becomes about 81,164.97. Adding 300 a month (108,000 of deposits) grows to roughly 447,000 combined.",
    faqs=[("What return should I assume?","Use a conservative real (after-inflation) return for planning; historical equity returns vary widely by period and market."),("Does compounding frequency matter much?","It matters less than rate and time. Moving from annual to monthly compounding adds a few percent over decades."),("What is the Rule of 72?","Divide 72 by the annual rate to estimate years to double: at 8%, about 9 years.")])

add(slug="simple-interest-calculator", cat="money", icon="➗", title="Simple Interest Calculator",
    short="Interest on principal only — for short loans, bonds and promissory notes.",
    inputs=[("P","Principal",5000,"cur","",100,""),("r","Annual rate",6,"","%",0.1,""),("t","Time",3,"","years",0.25,"")],
    js="""var I=v.P*v.r/100*v.t;return {results:[{l:'Interest',v:I,f:'money'},{l:'Total amount',v:v.P+I,f:'money'},{l:'Interest per year',v:v.P*v.r/100,f:'money'}]};""",
    formula="I = P × r × t\nTotal = P + I",
    intro="Simple interest is charged only on the original principal, so it grows in a straight line. It is common for short-term loans, some auto loans and fixed-coupon bonds.",
    example="5,000 at 6% for 3 years earns 5,000 × 0.06 × 3 = 900 in interest, for a total of 5,900.",
    faqs=[("How is it different from compound interest?","Compound interest earns interest on interest; simple interest never does, so it is always lower for the same rate and term over one period or more."),("Can time be in months?","Yes — enter months ÷ 12, e.g. 9 months = 0.75 years.")])

add(slug="savings-goal-calculator", cat="money", icon="🎯", title="Savings Goal Calculator",
    short="How much to save each month to hit a target by a deadline.",
    inputs=[("g","Savings goal",50000,"cur","",500,""),("cur0","Already saved",5000,"cur","",100,""),("r","Expected annual return",4,"","%",0.1,""),("y","Time to goal",5,"","years",0.5,"")],
    js="""var m=v.r/1200,n=Math.round(v.y*12),fvc=v.cur0*Math.pow(1+m,n),need=Math.max(0,v.g-fvc),p=m?need*m/(Math.pow(1+m,n)-1):need/n;
return {results:[{l:'Save each month',v:p,f:'money'},{l:'Total you will deposit',v:p*n,f:'money'},{l:'Growth does for you',v:Math.max(0,v.g-p*n-v.cur0),f:'money'},{l:'Current savings grow to',v:fvc,f:'money'}]};""",
    formula="Needed = Goal − Saved × (1+i)^n\nMonthly = Needed × i ÷ ((1+i)^n − 1)",
    intro="Work backwards from a target: the calculator grows what you already have, then finds the level monthly deposit that closes the gap.",
    example="To reach 50,000 in 5 years with 5,000 saved at 4%, you need roughly 662 a month.",
    faqs=[("What if my return is zero?","The tool simply divides the remaining gap by the number of months."),("Should I include an emergency fund?","Keep emergency cash separate from goal savings so a surprise expense does not derail the goal.")])

add(slug="investment-growth-calculator", cat="money", icon="🌱", title="Monthly Investment (SIP) Calculator",
    short="Systematic monthly investing with an optional yearly step-up.",
    inputs=[("c","Monthly investment",500,"cur","",10,""),("r","Expected annual return",10,"","%",0.1,""),("y","Duration",20,"","years",1,""),("s","Annual step-up",5,"","%",0.5,"Raise contribution yearly")],
    js="""var m=Math.pow(1+v.r/100,1/12)-1,b=0,dep=0,c=v.c,data=[];
for(var mo=1;mo<=v.y*12;mo++){b=b*(1+m)+c;dep+=c;if(mo%12===0){c*=1+v.s/100;if((mo/12)%Math.max(1,Math.round(v.y/15))===0)data.push({l:'Y'+mo/12,a:dep,b:Math.max(0,b-dep)})}}
return {results:[{l:'Portfolio value',v:b,f:'money'},{l:'Total invested',v:dep,f:'money'},{l:'Estimated gains',v:b-dep,f:'money'},{l:'Final monthly amount',v:c/(1+v.s/100),f:'money'}],series:{a:'Invested',b:'Gains',data:data}};""",
    formula="Each month: Balance = Balance × (1 + m) + Contribution\nm = (1 + annual rate)^(1/12) − 1; contribution rises by the step-up % each year",
    intro="A systematic investment plan (SIP) invests a fixed amount every month. A step-up raises that amount annually, usually in line with income — the single biggest lever after time.",
    example="500 a month at 10% for 20 years with a 5% annual step-up invests about 198,000 and can grow to roughly 511,000 under constant returns.",
    faqs=[("Are returns guaranteed?","No. Market returns vary; use this to compare scenarios, not as a forecast."),("Why use a step-up?","Contributions that grow with income compound on a larger base each year without feeling like a bigger sacrifice.")])

add(slug="retirement-calculator", cat="money", icon="🏖️", title="Retirement Calculator",
    short="Project your nest egg and the yearly income it can support.",
    inputs=[("a","Current age",35,"","",1,""),("ra","Retirement age",65,"","",1,""),("s","Current savings",50000,"cur","",1000,""),("c","Monthly contribution",800,"cur","",10,""),("r","Annual return",6,"","%",0.1,""),("w","Withdrawal rate",4,"","%",0.1,"Share withdrawn in year one")],
    js="""var n=Math.max(0,(v.ra-v.a)*12),m=Math.pow(1+v.r/100,1/12)-1,b=v.s,data=[];
for(var mo=1;mo<=n;mo++){b=b*(1+m)+v.c;if(mo%60===0)data.push({l:'Age '+(v.a+mo/12),a:b,b:0})}
return {results:[{l:'Projected nest egg',v:b,f:'money0'},{l:'Year-one income',v:b*v.w/100,f:'money0'},{l:'Monthly income',v:b*v.w/1200,f:'money0'},{l:'Years of saving',v:n/12,f:'years'}],series:{a:'Portfolio value',data:data}};""",
    formula="Nest egg = Savings × (1+m)^n + monthly contributions grown at m\nIncome = Nest egg × withdrawal rate",
    intro="Retirement planning is two numbers: what you accumulate and what you can safely draw. The widely discussed 4% guideline comes from historical US market studies; many planners now test 3–4% for longer retirements.",
    example="A 35-year-old with 50,000 saved, adding 800 a month at 6% until 65, projects to roughly 1.07 million — about 42,700 a year at a 4% withdrawal rate.",
    faqs=[("Is this in today's money?","No — it is nominal. Subtract expected inflation from your return to see the result in today's purchasing power."),("Does it include pensions or social security?","No. Add those income sources separately to the yearly income figure.")])

add(slug="inflation-calculator", cat="money", icon="🎈", title="Inflation Calculator",
    short="Future cost of today's money and how much purchasing power erodes.",
    inputs=[("A","Amount today",1000,"cur","",10,""),("r","Annual inflation",3,"","%",0.1,""),("y","Years",10,"","years",1,"")],
    js="""var f=Math.pow(1+v.r/100,v.y);return {results:[{l:'Same basket will cost',v:v.A*f,f:'money'},{l:'Today\\'s money will buy',v:v.A/f,f:'money'},{l:'Purchasing power lost',v:(1-1/f)*100,f:'pct'}]};""",
    formula="Future cost = A × (1 + r)^t\nReal value = A ÷ (1 + r)^t",
    intro="Inflation silently taxes cash. Use this to set salary targets, price contracts or understand why idle savings lose value.",
    example="At 3% inflation, something costing 1,000 today costs about 1,343.92 in 10 years, and 1,000 held in cash buys only about 744.09 of today's goods.",
    faqs=[("Which inflation rate should I use?","Use your country's recent consumer price index trend, or the central bank's target (often about 2%) for long horizons."),("How do I beat inflation?","Assets whose returns exceed inflation after tax maintain purchasing power; cash usually does not over long periods.")])

add(slug="credit-card-payoff-calculator", cat="money", icon="💳", title="Credit Card Payoff Calculator",
    short="Months to debt-free and total interest at your monthly payment.",
    inputs=[("B","Card balance",6000,"cur","",50,""),("apr","APR",22.9,"","%",0.1,""),("p","Monthly payment",250,"cur","",5,"")],
    js="""var i=v.apr/1200,b=v.B,n=0,I=0;if(v.p<=b*i)return {results:[{l:'Payoff time',v:'Never — payment ≤ monthly interest'},{l:'Minimum to make progress',v:b*i+1,f:'money'}]};
while(b>0.005&&n<1200){var it=b*i;I+=it;b=b+it-v.p;n++;}
return {results:[{l:'Months to debt-free',v:n,f:'int'},{l:'Total interest paid',v:I,f:'money'},{l:'Total paid',v:v.B+I,f:'money'},{l:'Interest in month 1',v:v.B*i,f:'money'}]};""",
    formula="Each month: Balance = Balance × (1 + APR/12) − Payment\nRepeat until the balance reaches zero",
    intro="Card APRs are among the most expensive debt most people carry. Small increases in your monthly payment cut both the timeline and the interest dramatically.",
    example="A 6,000 balance at 22.9% APR paid at 250 a month takes about 33 months and costs roughly 2,100 in interest.",
    faqs=[("Avalanche or snowball?","Avalanche (highest APR first) minimises interest; snowball (smallest balance first) builds momentum. Both beat minimum payments."),("Do balance transfers help?","A 0% promo can save a lot if you clear the balance before it ends — check the transfer fee.")])

add(slug="debt-to-income-calculator", cat="money", icon="⚖️", title="Debt-to-Income (DTI) Calculator",
    short="The ratio lenders use to judge whether you can take on more debt.",
    inputs=[("d","Monthly debt payments",1800,"cur","",10,"Housing, cards, loans"),("g","Gross monthly income",6500,"cur","",50,"")],
    js="""var x=v.g?v.d/v.g*100:0;return {results:[{l:'Debt-to-income ratio',v:x,f:'pct'},{l:'Assessment',v:x<=36?'Healthy (≤36%)':x<=43?'Stretched (36–43%)':'High (>43%)'},{l:'Room to 36%',v:Math.max(0,v.g*.36-v.d),f:'money'}]};""",
    formula="DTI = Monthly debt payments ÷ Gross monthly income × 100",
    intro="Many lenders look for a total DTI around 36% or lower, and 43% is a commonly cited upper limit for qualified mortgages in the US. Exact thresholds vary by lender and country.",
    example="1,800 of monthly debts on 6,500 gross income gives a DTI of about 27.7%.",
    faqs=[("Is rent included?","Lenders typically include housing payments; for a new mortgage they use the proposed payment."),("How do I lower DTI?","Pay down revolving balances, avoid new debt before applying, or raise documented income.")])

add(slug="profit-margin-calculator", cat="business", icon="💹", title="Profit Margin Calculator",
    short="Gross profit, margin and markup from cost and selling price.",
    inputs=[("c","Cost",60,"cur","",1,""),("p","Selling price",100,"cur","",1,"")],
    js="""var pr=v.p-v.c;return {results:[{l:'Profit margin',v:v.p?pr/v.p*100:0,f:'pct'},{l:'Profit',v:pr,f:'money'},{l:'Markup',v:v.c?pr/v.c*100:0,f:'pct'}],steps:'Margin = profit ÷ price; markup = profit ÷ cost. Same profit, different denominators.'};""",
    formula="Profit = Price − Cost\nMargin % = Profit ÷ Price × 100\nMarkup % = Profit ÷ Cost × 100",
    intro="Margin and markup describe the same profit from two angles. Confusing them is one of the most common pricing errors in small business — a 50% markup is only a 33.3% margin.",
    example="Cost 60, price 100: profit 40, margin 40%, markup 66.7%.",
    faqs=[("What is a good margin?","It depends on industry: software can exceed 70% gross margin while grocery retail often runs in single digits."),("Gross or net?","This is gross margin per unit. Net margin also subtracts overheads, interest and tax.")])

add(slug="markup-calculator", cat="business", icon="🏷️", title="Markup Calculator",
    short="Selling price from cost and markup — with the margin it really gives.",
    inputs=[("c","Cost",40,"cur","",1,""),("m","Markup",50,"","%",1,"")],
    js="""var p=v.c*(1+v.m/100);return {results:[{l:'Selling price',v:p,f:'money'},{l:'Profit',v:p-v.c,f:'money'},{l:'Resulting margin',v:p?(p-v.c)/p*100:0,f:'pct'}]};""",
    formula="Price = Cost × (1 + Markup%)",
    intro="Markup is how retailers often think; margin is how investors and accountants read your results. This shows both so your pricing targets line up with your financial targets.",
    example="A 40 cost with 50% markup sells at 60, earning 20 profit — a 33.3% margin.",
    faqs=[("Can markup exceed 100%?","Yes. Margin can never reach 100%, but markup can be any positive number."),("Keystone pricing?","Keystone means doubling cost: 100% markup, 50% margin.")])

add(slug="break-even-calculator", cat="business", icon="⚖️", title="Break-Even Calculator",
    short="Units and revenue needed to cover fixed costs.",
    inputs=[("F","Fixed costs (per month)",12000,"cur","",100,"Rent, salaries, software"),("p","Price per unit",40,"cur","",1,""),("vc","Variable cost per unit",16,"cur","",1,""),("t","Target profit (optional)",0,"cur","",100,"")],
    js="""var cm=v.p-v.vc;if(cm<=0)return {results:[{l:'Break-even',v:'Not possible — price ≤ variable cost'}]};var u=(v.F+v.t)/cm;
return {results:[{l:'Units to sell',v:Math.ceil(u),f:'int'},{l:'Revenue needed',v:u*v.p,f:'money0'},{l:'Contribution margin / unit',v:cm,f:'money'},{l:'Contribution margin ratio',v:cm/v.p*100,f:'pct'}]};""",
    formula="Break-even units = (Fixed costs + Target profit) ÷ (Price − Variable cost)\nBreak-even revenue = Units × Price",
    intro="Break-even analysis tells you the minimum volume a business needs before it makes a cent. It is the fastest sanity check on any pricing or cost decision.",
    example="Fixed costs 12,000, price 40, variable cost 16: each unit contributes 24, so you need 500 units (20,000 revenue) a month to break even.",
    faqs=[("How do I lower break-even?","Raise price, cut variable cost or reduce fixed costs — price changes usually move it most."),("Does it include tax?","No. Add tax as a fixed cost or use the target-profit field for a pre-tax goal.")])

add(slug="roi-calculator", cat="business", icon="🚀", title="ROI Calculator",
    short="Total and annualized return on any investment or campaign.",
    inputs=[("i","Amount invested",10000,"cur","",100,""),("f","Amount returned",15000,"cur","",100,""),("y","Holding period",3,"","years",0.25,"")],
    js="""var roi=v.i?(v.f-v.i)/v.i*100:0,ann=v.i&&v.y?(Math.pow(v.f/v.i,1/v.y)-1)*100:0;return {results:[{l:'Return on investment',v:roi,f:'pct'},{l:'Annualized return (CAGR)',v:ann,f:'pct'},{l:'Net gain',v:v.f-v.i,f:'money'}]};""",
    formula="ROI = (Final − Invested) ÷ Invested × 100\nCAGR = (Final ÷ Invested)^(1/years) − 1",
    intro="ROI compares outcomes; annualized return (CAGR) makes investments with different timelines comparable.",
    example="10,000 grows to 15,000 in 3 years: ROI 50%, annualized about 14.47%.",
    faqs=[("Why annualize?","A 50% return over 3 years is very different from 50% over 10 years — CAGR puts both on a yearly basis."),("What about cash flows in between?","For uneven cash flows use IRR; this calculator assumes one deposit and one withdrawal.")])

add(slug="cac-ltv-calculator", cat="business", icon="🧲", title="CAC & LTV Calculator",
    short="Customer acquisition cost, lifetime value, LTV:CAC and payback period.",
    inputs=[("s","Sales & marketing spend",15000,"cur","",100,"For the period"),("n","New customers",100,"","",1,"In the same period"),("a","Revenue per customer / month",30,"cur","",1,"ARPU"),("g","Gross margin",80,"","%",1,""),("ch","Monthly churn",4,"","%",0.1,"")],
    js="""var cac=v.n?v.s/v.n:0,gp=v.a*v.g/100,ltv=v.ch?gp/(v.ch/100):0;return {results:[{l:'LTV : CAC',v:cac?ltv/cac:0,f:'x'},{l:'Customer lifetime value',v:ltv,f:'money'},{l:'Customer acquisition cost',v:cac,f:'money'},{l:'CAC payback',v:gp?cac/gp:0,f:'months'},{l:'Avg. lifetime',v:v.ch?100/v.ch:0,f:'months'}]};""",
    formula="CAC = Spend ÷ New customers\nLTV = (ARPU × Gross margin) ÷ Monthly churn\nPayback = CAC ÷ (ARPU × Gross margin)",
    intro="Unit economics decide whether growth creates or destroys value. A common rule of thumb for subscription businesses is an LTV:CAC of 3× or higher with payback under 12 months.",
    example="CAC 150, ARPU 30 at 80% margin, 4% churn: LTV = 24 ÷ 0.04 = 600, LTV:CAC = 4×, payback 6.25 months.",
    faqs=[("Why gross margin, not revenue?","Revenue overstates value; only gross profit can repay acquisition cost."),("What churn should I use?","Use a recent cohort's monthly logo churn; blended numbers can hide weak cohorts.")])

add(slug="startup-runway-calculator", cat="business", icon="🛫", title="Startup Runway Calculator",
    short="How many months your cash lasts, with revenue growth.",
    inputs=[("cash","Cash in bank",120000,"cur","",1000,""),("e","Monthly expenses",15000,"cur","",100,""),("rv","Monthly revenue",3000,"cur","",100,""),("g","Revenue growth / month",5,"","%",0.5,"")],
    js="""var c=v.cash,r=v.rv,m=0,data=[],prof=null;while(c>0&&m<120){r=m?r*(1+v.g/100):r;c+=r-v.e;m++;if(prof===null&&r>=v.e)prof=m;if(m%3===0)data.push({l:'M'+m,a:Math.max(0,c),b:0})}
return {results:[{l:'Runway',v:m>=120?'10+ years':m,f:'months'},{l:'Net burn now',v:v.e-v.rv,f:'money'},{l:'Simple runway (no growth)',v:v.e>v.rv?v.cash/(v.e-v.rv):'Profitable',f:'months'},{l:'Month revenue covers costs',v:prof?('Month '+prof):'Not within runway'}],series:{a:'Cash balance',data:data}};""",
    formula="Each month: Cash = Cash + Revenue − Expenses; Revenue grows by g%\nSimple runway = Cash ÷ (Expenses − Revenue)",
    intro="Runway is survival time. Most investors advise raising with at least 6–9 months of runway left, because fundraising itself takes months.",
    example="120,000 cash, 15,000 expenses and 3,000 revenue gives 10 months of simple runway; at 5% monthly revenue growth the runway extends to about 11 months.",
    faqs=[("Gross or net burn?","Net burn (expenses minus revenue) is what drains cash; gross burn shows your cost base."),("How do I extend runway?","Cut the largest fixed costs first, raise prices, or collect receivables faster.")])

add(slug="pricing-calculator", cat="business", icon="🧮", title="Price From Target Margin",
    short="The price you must charge to hit a target gross margin.",
    inputs=[("c","Unit cost",35,"cur","",1,""),("m","Target margin",45,"","%",1,"")],
    js="""if(v.m>=100)return {results:[{l:'Price',v:'Margin must be below 100%'}]};var p=v.c/(1-v.m/100);return {results:[{l:'Required price',v:p,f:'money'},{l:'Profit per unit',v:p-v.c,f:'money'},{l:'Equivalent markup',v:v.c?(p-v.c)/v.c*100:0,f:'pct'}]};""",
    formula="Price = Cost ÷ (1 − Target margin)",
    intro="Set prices from the margin you need rather than from a habit markup. The equivalent markup is shown so you can communicate it to buyers or retail partners.",
    example="A 35 cost at a 45% target margin requires a price of about 63.64.",
    faqs=[("Why not cost × (1 + margin)?","That calculates markup, which yields a lower margin than you intended."),("Should I round?","Psychological pricing (e.g. ending in .99 or 8 in some markets) can lift conversions — round up after calculating.")])

add(slug="discount-calculator", cat="everyday", icon="🛍️", title="Discount Calculator",
    short="Sale price with stacked discounts and what you really save.",
    inputs=[("p","Original price",120,"cur","",1,""),("d","Discount",25,"","%",1,""),("e","Extra discount",10,"","%",1,"Applied after the first")],
    js="""var f=v.p*(1-v.d/100)*(1-v.e/100);return {results:[{l:'Final price',v:f,f:'money'},{l:'You save',v:v.p-f,f:'money'},{l:'Effective discount',v:v.p?(1-f/v.p)*100:0,f:'pct'}]};""",
    formula="Final = Price × (1 − d1) × (1 − d2)",
    intro="Stacked discounts multiply rather than add: 25% then 10% is 32.5% off, not 35%.",
    example="120 with 25% off then an extra 10% off costs 81 — an effective 32.5% discount.",
    faqs=[("Does order matter?","No — multiplication is commutative, so 10% then 25% gives the same result."),("Is tax applied before or after?","Usually after discounts; use the sales-tax calculator on the final price.")])

add(slug="sales-tax-calculator", cat="everyday", icon="🧾", title="Sales Tax / GST / VAT Calculator",
    short="Add tax to a net price or extract tax from a tax-inclusive price.",
    inputs=[("a","Amount",100,"cur","",1,""),("t","Tax rate",13,"","%",0.1,"e.g. HST, GST, VAT"),("mode","Mode","add","select",[("add","Add tax to amount"),("remove","Remove tax from amount")],None,"")],
    js="""var r=v.t/100;if(v.mode==='remove'){var net=v.a/(1+r);return {results:[{l:'Net (before tax)',v:net,f:'money'},{l:'Tax included',v:v.a-net,f:'money'},{l:'Gross',v:v.a,f:'money'}]}}
return {results:[{l:'Total with tax',v:v.a*(1+r),f:'money'},{l:'Tax',v:v.a*r,f:'money'},{l:'Net',v:v.a,f:'money'}]};""",
    formula="Add: Total = Net × (1 + rate)\nRemove: Net = Gross ÷ (1 + rate)",
    intro="Removing tax is not the same as subtracting the rate — to extract 13% tax from a gross price you divide by 1.13.",
    example="100 plus 13% tax is 113. Removing 13% from 113 returns a net of 100 and tax of 13.",
    faqs=[("Why can't I just subtract 13%?","Because the tax was calculated on the smaller net amount, not on the gross."),("Which rate applies to me?","Rates vary by country, province or state and by product category — check your tax authority.")])

add(slug="freelance-rate-calculator", cat="business", icon="🧑‍💻", title="Freelance Hourly Rate Calculator",
    short="The hourly rate that actually pays your target income after costs and tax.",
    inputs=[("inc","Target take-home income / year",70000,"cur","",1000,""),("exp","Business expenses / year",8000,"cur","",100,""),("tax","Tax rate",25,"","%",1,""),("h","Billable hours / week",25,"","",1,""),("w","Working weeks / year",46,"","",1,"")],
    js="""var hrs=v.h*v.w,gross=(v.inc/(1-v.tax/100))+v.exp,rate=hrs?gross/hrs:0;return {results:[{l:'Minimum hourly rate',v:rate,f:'money'},{l:'Day rate (8h)',v:rate*8,f:'money'},{l:'Revenue needed',v:gross,f:'money0'},{l:'Billable hours / year',v:hrs,f:'int'}]};""",
    formula="Revenue = Income ÷ (1 − tax) + Expenses\nRate = Revenue ÷ (Billable hours × Weeks)",
    intro="Freelancers rarely bill 40 hours a week — admin, sales and gaps eat time. Pricing from billable hours prevents the classic under-charging trap.",
    example="70,000 take-home at 25% tax plus 8,000 expenses requires about 101,333 revenue; at 25 billable hours for 46 weeks that is about 88 per hour.",
    faqs=[("How many hours are billable?","Many freelancers bill 50–70% of their working hours."),("Should I charge by project?","Value-based project pricing often earns more, but this rate is your floor.")])

add(slug="salary-converter", cat="everyday", icon="💼", title="Hourly ↔ Salary Converter",
    short="Convert an hourly wage to weekly, monthly and annual pay.",
    inputs=[("r","Hourly rate",28,"cur","",0.5,""),("h","Hours per week",40,"","",1,""),("w","Paid weeks per year",52,"","",1,"")],
    js="""var y=v.r*v.h*v.w;return {results:[{l:'Annual pay',v:y,f:'money0'},{l:'Monthly pay',v:y/12,f:'money'},{l:'Bi-weekly pay',v:y/26,f:'money'},{l:'Weekly pay',v:v.r*v.h,f:'money'}]};""",
    formula="Annual = Hourly × Hours/week × Weeks/year",
    intro="A quick way to compare job offers quoted in different units. Remember benefits and paid leave when comparing hourly and salaried roles.",
    example="28 per hour at 40 hours for 52 weeks is 58,240 a year, or about 4,853 a month.",
    faqs=[("What about overtime?","Add overtime hours separately at the overtime multiplier."),("Gross or net?","This is gross pay before deductions.")])

add(slug="adsense-revenue-calculator", cat="web-ai", icon="📰", title="Ad Revenue (RPM) Calculator",
    short="Estimate display-ad earnings from pageviews and page RPM, with growth.",
    inputs=[("pv","Monthly pageviews",50000,"","",1000,""),("rpm","Page RPM",8,"cur","",0.5,"Earnings per 1,000 pageviews"),("g","Traffic growth / month",5,"","%",0.5,"")],
    js="""var m=v.pv/1000*v.rpm,t=0,pv=v.pv,data=[];for(var i=1;i<=12;i++){var e=pv/1000*v.rpm;t+=e;data.push({l:'M'+i,a:e,b:0});pv*=1+v.g/100}
return {results:[{l:'Revenue this month',v:m,f:'money'},{l:'Next 12 months (with growth)',v:t,f:'money0'},{l:'Pageviews in month 12',v:pv/(1+v.g/100),f:'int'},{l:'Revenue per 100 visits',v:v.rpm/10,f:'money'}],series:{a:'Monthly ad revenue',data:data}};""",
    formula="Revenue = Pageviews ÷ 1,000 × Page RPM",
    intro="Page RPM bundles CTR, CPC and ad density into one number. It varies hugely by niche and audience geography — finance and insurance content typically earns far more than entertainment.",
    example="50,000 monthly pageviews at an 8 RPM earns about 400 a month.",
    faqs=[("What RPM should I expect?","Ranges are wide; check your own analytics once live. Niche, country and season matter more than the ad network."),("How do I raise RPM?","Target higher-value topics, improve engagement and page speed, and serve audiences in higher-value markets.")])

add(slug="website-valuation-calculator", cat="web-ai", icon="🏛️", title="Website Valuation Calculator",
    short="Estimate a content site's sale value from profit and an earnings multiple.",
    inputs=[("p","Average monthly net profit",1500,"cur","",50,"Last 6–12 months"),("mult","Earnings multiple","36","select",[("24","24× — new or volatile"),("30","30× — some history"),("36","36× — stable"),("42","42× — strong, diversified"),("48","48× — premium")],None,"Months of profit")],
    js="""var val=v.p*v.mult;return {results:[{l:'Estimated value',v:val,f:'money0'},{l:'Annual profit',v:v.p*12,f:'money0'},{l:'Low – high range',v:(function(){var l=v.p*(v.mult-6),h=v.p*(+v.mult+6);return l.toLocaleString(undefined,{maximumFractionDigits:0})+' – '+h.toLocaleString(undefined,{maximumFractionDigits:0})})()},{l:'Payback for buyer',v:v.mult/12,f:'years'}]};""",
    formula="Value = Average monthly net profit × Multiple",
    intro="Content and ad-supported websites are commonly valued as a multiple of average monthly net profit. The multiple depends on age, traffic diversity, trend, and how much owner time the site needs.",
    example="A site netting 1,500 a month at a 36× multiple is valued around 54,000.",
    faqs=[("What raises the multiple?","Longer history, growing traffic, several revenue streams, low owner hours and clean documentation."),("Is the domain included?","Usually yes — premium domains can add value beyond the earnings multiple.")])

add(slug="domain-flip-calculator", cat="web-ai", icon="🌐", title="Domain Flip Profit Calculator",
    short="Net profit and annualized return on buying, holding and selling a domain.",
    inputs=[("b","Purchase price",500,"cur","",10,""),("rn","Renewal / year",12,"cur","",1,""),("y","Years held",3,"","years",0.5,""),("s","Sale price",3500,"cur","",50,""),("c","Marketplace commission",15,"","%",0.5,"")],
    js="""var cost=v.b+v.rn*v.y,net=v.s*(1-v.c/100),p=net-cost;return {results:[{l:'Net profit',v:p,f:'money'},{l:'ROI',v:cost?p/cost*100:0,f:'pct'},{l:'Annualized return',v:cost&&v.y?(Math.pow(Math.max(net,0)/cost,1/v.y)-1)*100:0,f:'pct'},{l:'Total cost basis',v:cost,f:'money'}]};""",
    formula="Cost basis = Purchase + Renewal × Years\nNet sale = Sale price × (1 − Commission)\nProfit = Net sale − Cost basis",
    intro="Domain investing is a portfolio game: holding costs compound across hundreds of names, so each sale must cover the renewals of the names that never sell.",
    example="Buy at 500, renew at 12 for 3 years, sell at 3,500 with 15% commission: net sale 2,975, cost 536, profit 2,439.",
    faqs=[("What sell-through rate is typical?","Portfolio investors often report low single-digit annual sell-through; price your names to cover portfolio-wide renewals."),("Should I include my time?","For a business view, yes — add an hourly cost for outbound sales effort.")])

add(slug="ai-token-cost-calculator", cat="web-ai", icon="🧠", title="AI API Token Cost Calculator",
    short="Monthly cost of an AI feature from requests, tokens and per-million pricing.",
    inputs=[("q","Requests per day",1000,"","",10,""),("ti","Input tokens / request",800,"","",10,"Prompt + context"),("to","Output tokens / request",400,"","",10,""),("pi","Price / 1M input tokens",3,"cur","",0.05,"From your provider"),("po","Price / 1M output tokens",15,"cur","",0.05,"")],
    js="""var per=v.ti/1e6*v.pi+v.to/1e6*v.po,d=per*v.q;return {results:[{l:'Monthly cost (30 days)',v:d*30,f:'money'},{l:'Daily cost',v:d,f:'money'},{l:'Cost per 1,000 requests',v:per*1000,f:'money'},{l:'Requests per 1 unit of currency',v:per?Math.floor(1/per):0,f:'int'}]};""",
    formula="Cost/request = Input tokens × Input price/1M + Output tokens × Output price/1M\nMonthly = Cost/request × Requests/day × 30",
    intro="AI providers price per million tokens, usually with output tokens costing several times more than input. Long prompts and verbose outputs are the two main cost drivers.",
    example="1,000 requests a day with 800 input and 400 output tokens at 3 and 15 per million costs 0.0084 per request, about 252 a month.",
    faqs=[("How do I cut costs?","Trim system prompts, cache repeated context where your provider supports it, cap output length and route simple tasks to smaller models."),("What is a token?","Roughly ¾ of an English word on average; exact counts depend on the model's tokenizer.")])

add(slug="ai-roi-calculator", cat="web-ai", icon="⚙️", title="AI Automation ROI Calculator",
    short="Value of hours saved by AI tools versus their monthly cost.",
    inputs=[("h","Hours saved / person / week",4,"","",0.5,""),("n","People using it",5,"","",1,""),("c","Loaded hourly cost",45,"cur","",1,"Salary + overhead"),("t","Tool cost / month (total)",300,"cur","",10,""),("a","Adoption rate",70,"","%",5,"Share who actually use it")],
    js="""var val=v.h*v.n*(v.a/100)*v.c*52/12,net=val-v.t;return {results:[{l:'Net monthly value',v:net,f:'money'},{l:'Gross value of time saved',v:val,f:'money'},{l:'ROI',v:v.t?net/v.t*100:0,f:'pct'},{l:'Hours saved / month',v:v.h*v.n*(v.a/100)*52/12,f:'int'}]};""",
    formula="Value = Hours saved × People × Adoption × Hourly cost × 52 ÷ 12\nNet = Value − Tool cost",
    intro="AI ROI hinges on adoption more than capability. A tool that saves 4 hours a week but is used by half the team delivers half the value — model it honestly.",
    example="4 hours × 5 people × 70% adoption × 45 per hour ≈ 2,730 of monthly value; minus 300 of tools is about 2,430 net.",
    faqs=[("Is saved time real savings?","Only if it is redeployed to revenue work or avoids hiring; otherwise treat it as capacity."),("What about quality?","Add review time for AI output to keep the estimate realistic.")])

add(slug="youtube-earnings-calculator", cat="web-ai", icon="▶️", title="YouTube Earnings Calculator",
    short="Estimate creator ad income from monthly views and RPM.",
    inputs=[("v","Monthly views",200000,"","",1000,""),("rpm","RPM (creator earnings per 1,000 views)",3,"cur","",0.1,"")],
    js="""var m=v.v/1000*v.rpm;return {results:[{l:'Monthly earnings',v:m,f:'money'},{l:'Yearly earnings',v:m*12,f:'money0'},{l:'Daily earnings',v:m/30,f:'money'}]};""",
    formula="Earnings = Views ÷ 1,000 × RPM",
    intro="RPM is what the creator actually receives per thousand views after the platform's share. It varies by topic, audience country and format.",
    example="200,000 monthly views at a 3 RPM is about 600 a month or 7,200 a year.",
    faqs=[("RPM vs CPM?","CPM is what advertisers pay per 1,000 ad impressions; RPM is creator revenue per 1,000 total views."),("Other income?","Sponsorships, memberships and affiliate links often out-earn ads for niche channels.")])

add(slug="affiliate-earnings-calculator", cat="web-ai", icon="🔗", title="Affiliate Earnings Calculator",
    short="Commission income from traffic, click-through and conversion rates.",
    inputs=[("t","Monthly visitors",20000,"","",100,""),("ctr","Click-through to offer",8,"","%",0.5,""),("cr","Conversion rate",3,"","%",0.1,""),("aov","Average order value",120,"cur","",1,""),("com","Commission",8,"","%",0.5,"")],
    js="""var cl=v.t*v.ctr/100,s=cl*v.cr/100,e=s*v.aov*v.com/100;return {results:[{l:'Monthly commissions',v:e,f:'money'},{l:'Clicks to merchant',v:cl,f:'int'},{l:'Sales',v:s,f:'int'},{l:'Earnings per 1,000 visitors',v:v.t?e/v.t*1000:0,f:'money'}]};""",
    formula="Earnings = Visitors × CTR × Conversion × Order value × Commission",
    intro="Affiliate revenue is a funnel; improving any stage multiplies the result. Earnings per visitor lets you compare affiliate pages against ad RPM.",
    example="20,000 visitors × 8% CTR × 3% conversion × 120 order × 8% commission ≈ 461 a month.",
    faqs=[("What moves the needle most?","Buyer-intent traffic (comparisons, reviews) lifts both CTR and conversion."),("Ads or affiliates?","Use both, but avoid ads near your highest-converting affiliate links.")])

add(slug="lead-value-calculator", cat="web-ai", icon="🎣", title="Lead Value & Cost Calculator",
    short="What each lead is worth — and the most you can afford to pay for one.",
    inputs=[("l","Leads per month",80,"","",1,""),("c","Close rate",15,"","%",0.5,""),("d","Average deal value",1200,"cur","",10,""),("cpl","Cost per lead",25,"cur","",1,"")],
    js="""var s=v.l*v.c/100,rev=s*v.d,vpl=v.c/100*v.d,cost=v.l*v.cpl;return {results:[{l:'Value per lead',v:vpl,f:'money'},{l:'Monthly revenue from leads',v:rev,f:'money0'},{l:'Lead cost',v:cost,f:'money0'},{l:'Return on lead spend',v:cost?(rev-cost)/cost*100:0,f:'pct'}]};""",
    formula="Value per lead = Close rate × Deal value\nReturn = (Revenue − Lead cost) ÷ Lead cost",
    intro="Knowing the value per lead turns marketing into arithmetic: any channel that delivers leads below that value (after margin) is worth scaling.",
    example="15% close rate on a 1,200 deal makes each lead worth 180. Buying 80 leads at 25 costs 2,000 and returns about 14,400 in revenue.",
    faqs=[("Revenue or profit?","For a strict ceiling on cost per lead, use gross profit per deal instead of revenue."),("How do I raise close rate?","Faster response times and qualifying questions in your form lift close rates more than anything else.")])

add(slug="conversion-rate-calculator", cat="web-ai", icon="🎯", title="Conversion Rate Calculator",
    short="Conversion rate and the traffic you need to hit a goal.",
    inputs=[("v","Visitors",12000,"","",100,""),("c","Conversions",240,"","",1,""),("g","Goal conversions",500,"","",1,"")],
    js="""var r=v.v?v.c/v.v:0;return {results:[{l:'Conversion rate',v:r*100,f:'pct'},{l:'Visitors needed for goal',v:r?v.g/r:0,f:'int'},{l:'Or rate needed at current traffic',v:v.v?v.g/v.v*100:0,f:'pct'}]};""",
    formula="Conversion rate = Conversions ÷ Visitors × 100",
    intro="Two levers reach any goal: more traffic or a higher conversion rate. This shows the size of each gap so you can choose the cheaper one.",
    example="240 conversions from 12,000 visitors is 2%. To reach 500 you need 25,000 visitors, or a 4.17% rate on current traffic.",
    faqs=[("What is a good conversion rate?","It depends on offer and traffic source; compare against your own history rather than generic benchmarks."),("Micro-conversions?","Track newsletter signups and calculator uses too — they predict later sales.")])

add(slug="percentage-calculator", cat="everyday", icon="％", title="Percentage Calculator",
    short="X% of Y, what percent A is of B, and the reverse.",
    inputs=[("p","Percent",15,"","%",0.1,""),("y","Of value",240,"","",1,""),("a","Part (for “A is what % of B”)",36,"","",1,""),("b","Whole",240,"","",1,"")],
    js="""return {results:[{l:v.p+'% of '+v.y,v:v.p/100*v.y,f:'num'},{l:v.a+' is what % of '+v.b,v:v.b?v.a/v.b*100:0,f:'pct'},{l:v.y+' is '+v.p+'% of',v:v.p?v.y/(v.p/100):0,f:'num'}]};""",
    formula="X% of Y = X ÷ 100 × Y\nA as % of B = A ÷ B × 100",
    intro="Three of the most-searched percentage questions answered at once — no mode switching.",
    example="15% of 240 is 36; 36 is 15% of 240; and 240 is 15% of 1,600.",
    faqs=[("Percent vs percentage points?","Going from 10% to 12% is a 2 percentage-point rise but a 20% relative increase."),("Shortcut for 10%?","Move the decimal one place left: 10% of 240 is 24.")])

add(slug="percentage-change-calculator", cat="everyday", icon="↕️", title="Percentage Change Calculator",
    short="Increase or decrease between two values, as a percent.",
    inputs=[("o","Old value",80,"","",1,""),("n","New value",100,"","",1,"")],
    js="""var ch=v.o?(v.n-v.o)/Math.abs(v.o)*100:0;return {results:[{l:'Percentage change',v:ch,f:'pct'},{l:'Absolute change',v:v.n-v.o,f:'num'},{l:'Reverse change (new → old)',v:v.n?(v.o-v.n)/Math.abs(v.n)*100:0,f:'pct'}]};""",
    formula="Change % = (New − Old) ÷ |Old| × 100",
    intro="A 25% rise followed by a 20% fall returns you to the start — percentage changes are not symmetric. The reverse change shows exactly that.",
    example="From 80 to 100 is +25%; from 100 back to 80 is −20%.",
    faqs=[("Why is the reverse different?","Each change is measured against a different starting value."),("What if old is zero?","Percentage change from zero is undefined.")])

add(slug="tip-calculator", cat="everyday", icon="🍽️", title="Tip & Bill Split Calculator",
    short="Tip amount and each person's share.",
    inputs=[("b","Bill",86,"cur","",1,""),("t","Tip",18,"","%",1,""),("p","People",3,"","",1,"")],
    js="""var tip=v.b*v.t/100,tot=v.b+tip;return {results:[{l:'Each person pays',v:v.p?tot/v.p:tot,f:'money'},{l:'Tip',v:tip,f:'money'},{l:'Total',v:tot,f:'money'}]};""",
    formula="Tip = Bill × Tip%\nPer person = (Bill + Tip) ÷ People",
    intro="Tipping customs differ widely by country — from 15–20% in the US and Canada to small or no tips elsewhere.",
    example="An 86 bill with an 18% tip is 101.48 total, about 33.83 each for three people.",
    faqs=[("Tip before or after tax?","Customs vary; many people tip on the pre-tax amount."),("Round up?","Rounding each share to a whole number keeps splitting simple.")])

add(slug="unit-price-calculator", cat="everyday", icon="⚖️", title="Unit Price Comparison",
    short="Which pack size is really cheaper per unit.",
    inputs=[("pa","Price A",4.99,"cur","",0.01,""),("qa","Quantity A",500,"","",1,"grams, ml, items…"),("pb","Price B",8.49,"cur","",0.01,""),("qb","Quantity B",1000,"","",1,"")],
    js="""var ua=v.qa?v.pa/v.qa:0,ub=v.qb?v.pb/v.qb:0,best=ua<=ub?'A':'B',sv=Math.max(ua,ub)?Math.abs(ua-ub)/Math.max(ua,ub)*100:0;return {results:[{l:'Better value',v:'Option '+best+' ('+sv.toFixed(1)+'% cheaper per unit)'},{l:'Price per 100 units — A',v:ua*100,f:'money'},{l:'Price per 100 units — B',v:ub*100,f:'money'}]};""",
    formula="Unit price = Price ÷ Quantity",
    intro="Bigger packs are not always cheaper per unit. Comparing unit prices is the simplest way to stop overpaying.",
    example="4.99 for 500 g is 0.00998 per gram; 8.49 for 1,000 g is 0.00849 — the larger pack is about 14.9% cheaper per gram.",
    faqs=[("Same units?","Make sure both quantities use the same unit before comparing."),("Waste?","A cheaper unit price only helps if you use it all before it expires.")])
