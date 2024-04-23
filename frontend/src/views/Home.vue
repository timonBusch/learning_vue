<script setup lang="ts">
import { ref } from "vue"
import { useFetch } from "@vueuse/core";
import '@vuepic/vue-datepicker/dist/main.css'

const email = ref()
const fullname = ref()
const phone_number = ref()
const company_name = ref()

const new_customer = ref({
  email: email,
  full_name: fullname,
  phone: phone_number,
  company: company_name
})

const enableButton = ref()

function createCustomer(event: Event) {
  if(event) {
    const url = "http://127.0.0.1:8000/customers/"
    
    useFetch(url).post(new_customer)
 
  }
}

function validateInputs(event: Event) {
  if(event) {
    enableButton.value = email.value && fullname.value && phone_number.value && company_name.value
  }
}

</script>

<template>
    <div class="mt-3">
      <form>
        <div class="row mb-3">
          <label for="inputEmail" class="col-sm-2 col-form-label">Email</label>
          <div class="col-sm-10">
            <input @input="validateInputs" v-model="email" type="text" class="form-control" id="inputEmail">
          </div>
        </div>
        <div class="row mb-3">
          <label for="inputName" class="col-sm-2 col-form-label">Fullname</label>
          <div class="col-sm-10">
            <input @input="validateInputs" v-model="fullname" type="text" class="form-control" id="inputName">
          </div>
        </div>
        <div class="row mb-3">
          <label for="inputPhone" class="col-sm-2 col-form-label">Phone Number</label>
          <div class="col-sm-10">
            <input @input="validateInputs" v-model="phone_number" type="text" class="form-control" id="inputPhone">
          </div>
        </div>
        <div class="row mb-3">
          <label for="inputCompany" class="col-sm-2 col-form-label">Company Name</label>
          <div class="col-sm-10">
            <input @input="validateInputs" v-model="company_name" type="text" class="form-control" id="inputCompany">
          </div>
        </div>
        <button @click="createCustomer" type="button" class="btn btn-primary" :class="{disabled: !enableButton}">Create Customer</button>
      </form>
    </div>  

</template>
  