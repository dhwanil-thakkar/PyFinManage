<!-- Investments in a portfolio.vue -->
<template>
    <div id="InvestmentsContainer" class="container p-4">
      
      
      <h2 class="text-4xl p-4">Selected Portfolio: {{ selectedPortfolioName || 'Please click on a portfolio to select' }}</h2>
      
      <div id="Porfolio-actions" class="flex justify-between">

        <button @click="fetchAllInvestments" class="border bg-black  m-4 p-4 text-white">
          Click Here to refresh investments
        </button>

        <div v-if="selectedPortfolioName">
          <BuyOrSellInvestmentPopUp
            :selectedPortfolio = "selectedPortfolioName"
          />
        </div>
      </div>
      

    <div v-if="investments.length" class="flex flex-col space-y-8 m-8 p-8 ">
      <table class="w-full">
        <thead>
          <tr class="bg-gray-100">
            <th>Name</th>
            <th>Quantity </th>
            <th>Average Price</th>
            <th>Market Price</th>
            <th>+/- % Change</th>
            <th>Last Updated At </th>
          </tr>
        </thead>
        <tbody>
          <InvestmentItemTableFormat
            v-for="investment in investments" 
            :key="investment.investment_id" 
            :investment="investment" 
          />
        </tbody>
      </table>
    </div>
    
    <!-- Display a message if there are no investments -->
    <p v-else>No investments found for this portfolio.</p>


    </div>
  </template>
  
  <script>
  import axios from 'axios';
  import InvestmentItemTableFormat from './InvestmentItemTableFormat.vue';
  import BuyOrSellInvestmentPopUp from './BuyOrSellInvestmentPopUp.vue';

  export default {
    props: {
      selectedPortfolioName: {
        type: String,
        default: ''
      }
    },
    components: {
      InvestmentItemTableFormat,
      BuyOrSellInvestmentPopUp
    },
    data(){
      return{
        investments: []
      };
    },
    methods: {
      fetchAllInvestments() {
        axios.get(`http://127.0.0.1:8000/portfolio/${this.selectedPortfolioName}/investments`)
        .then(response => {
          this.investments = response.data.holdings;
          console.log(response.data);
        })
        .catch(error => {
          console.log('Error: ', error)
        });
      },
    },
    watch: {
      selectedPortfolioName(newVal) {
        this.investment = [];
        if(newVal) {
          this.fetchAllInvestments();
        }
      }
    }
  };
  </script>