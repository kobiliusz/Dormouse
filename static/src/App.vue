<template>
  <div>
    <div id="topbar">
      <label for="room-list">Room</label>
      <select @change="selectRoom($event)" name="room-list" id="room-list">
        <option v-for="room in rooms" :key="room.id">{{ room.name }}</option>
      </select>
      <label for="nick-input">Nick</label>
      <input type="text" id="nick-input" v-model="nick" placeholder="enter nick"/>
    </div>
    <div id="messagelist">

    </div>
    <div id="bottombar">
      <label for="content-input">Message</label>
      <input type="text" id="content-input" v-model="prompt" placeholder="enter message"
      @keydown="enterMessage($event)" :disabled="!nick"/>
      <button id="send-button" :disabled="!nick" @click="sendMessage()">Send</button>
    </div>
  </div>
</template>

<script>
import axios from "axios";
export default {
  
  data() {
    return {
      rooms: [],
      room_id: 1,
      messages: [],
      nick: '',
      prompt: ''
    }
  },
  
  methods: {
    getRooms() {
      axios.get('http://localhost:80/api/rooms')
        .then(response => {
          this.rooms = response.data
        }).catch(error => {
          console.log(error)
        })
    },
    selectRoom(event) {
      this.room_id = event.target.key
    },
    getMessages() {
      axios.get(`http://localhost:80/api/messages/${this.room_id}`)
        .then(response => {
          this.messages = response.data
        }).catch(error => {
          console.log(error)
        })
    },
    enterMessage(event) {
      if (event.keyCode == 13) {
        this.sendMessage()
      }
    },
    sendMessage() {
      axios.post(`http://localhost:80/api/messages/${this.room_id}`, {
        nick: this.nick,
        content: this.prompt
      })
        .then(response => {
          console.log(response.data)
          this.prompt = ''
        }).catch(error => {
          console.log(error)
          this.prompt = ''
        })
    }
    
  },
  

  mounted() {
    this.getRooms()
    this.getMessages()
  }

}
</script>

<style>

</style>
