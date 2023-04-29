<template>
  <div>
    <div id="topbar">
      <h1 class="whtxt">Dormouse</h1>
      <label for="room-list" class="whtxt">Room</label>
      <select v-model="room_id" name="room-list" id="room-list" @change="getMessages()">
        <option v-for="room in rooms" :key="room.id"
          :value="room.id">{{ room.name }}</option>
      </select>
      <label for="nick-input" class="whtxt">Nick</label>
      <input type="text" id="nick-input" v-model="nick" placeholder="enter nick"/>
    </div>
    <div id="messagelist">
      <message-row v-for="message in messages" :key="message.id" :content="message.content"
        :nick="message.nick" :timestamp="message.time"/>
    </div>
    <div id="bottombar">
      <div id="bottom-content">
        <label for="content-input" class="whtxt">Message</label>
        <input type="text" id="content-input" v-model="prompt" placeholder="enter message"
          @keydown="enterMessage($event)" :disabled="!nick"/>
        <button id="send-button" :disabled="!nick || !prompt" @click="sendMessage()">Send</button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import MessageRow from "./components/MessageRow.vue";
export default {
  
  components: {
    MessageRow,
  },

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
      if (this.prompt.trim().length > 0) {
        axios.post(`http://localhost:80/api/messages/${this.room_id}`, {
          nick: this.nick,
          content: this.prompt
        })
          .then(response => {
            console.log(response.data)
            this.prompt = ''
            this.getMessages()
          }).catch(error => {
            console.log(error)
            this.prompt = ''
          })
      }
    },
    
  },

  mounted() {
    this.getRooms()
    this.getMessages()
    setInterval(this.getMessages, 1000)
  },

}
</script>

<style>
  body {
    font-family: Verdana, Geneva, Tahoma, sans-serif;
  }
  #topbar {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 125px;
    background-color: #22a34d;
  }
  #messagelist {
    position: fixed;
    top: 125px;
    width: 100%;
    bottom: 40px;
    overflow: auto;
  }
  #bottombar {
    position: fixed;
    bottom: 0;
    left: 0;
    width: 100%;
    height: 40px;
    background-color: #22a34d;
  }
  #bottom-content {
    padding-top: 10px;
  }
  .whtxt {
    color: #fff;
  }
  label {
    padding: 15px;
    padding-right: 7px;
  }
  h1 {
    padding-left: 15px;
  }
  #content-input {
    width: 350px;
  }
  #nick-input {
    width: 150px;
  }
  #room-list {
    width: 150px;
  }
</style>
