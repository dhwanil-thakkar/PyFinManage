<!-- Investments.vue -->
<template>
    <div id="InvestmentsContainer" class="container p-4">
      
      
      <h2 class="text-4xl p-4">Selected Portfolio: {{ selectedPortfolioName || 'Please click on a portfolio to select' }}</h2>
      
      
      
      <button @click="fetchAllInvestments" class="border bg-black m-4 p-4 text-white">
        Click Here to refresh investments
      </button>


    <div v-if="investments.length" class="flex flex-col space-y-8 m-8 p-8 ">
      <!-- <InvestmentItem 
        v-for="investment in investments" 
        :key="investment.investment_id" 
        :investment="investment" 
      /> -->
      <table class="w-full">
        <thead>
          <tr class="bg-gray-100">
            <th>Name</th>
            <th>Average Price</th>
            <th>Current Price</th>
            <th>Quantity </th>
            <th>Last Updated At </th>
            <th>Actions </th>
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
  import InvestmentItem from './InvestmentItem.vue';
  import InvestmentItemTableFormat from './InvestmentItemTableFormat.vue';

  export default {
    props: {
      selectedPortfolioName: {
        type: String,
        default: ''
      }
    },
    components: {
      InvestmentItem,
      InvestmentItemTableFormat
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
      SelectInvestment(){
        this.$emit('investment-selected', investment);    // Emit an event with the selected investment
      }
    }
  };
  </script>