<template>
  <div>
    <div id="topbar">
      <h1 class="whtxt">Dormouse</h1>
      <label for="room-list" class="whtxt">Room</label>
      <select v-model="room_id" name="room-list" id="room-list" @change="getMessages">
        <option v-for="room in rooms" :key="room.id"
          :value="room.id">{{ room.name }}</option>
      </select>
      <label for="nick-input" class="whtxt">Nick</label>
      <input type="text" id="nick-input" v-model="nick" 
        placeholder="enter nick" @change="storeNick"/>
      <img src="./assets/logo.png" id="logo"/>
    </div>
    <div id="messagelist" ref="msglist">
      <message-row v-for="message in messages" :key="message.id" :content="message.content"
        :nick="message.nick" :timestamp="message.time"/>
    </div>
    <div id="bottombar">
      <div id="bottom-content">
        <label for="content-input" class="whtxt">Message</label>
        <input type="text" id="content-input" v-model="prompt" placeholder="enter message"
          @keypress.enter="sendMessage" :disabled="!nick" ref="contentinput"/>
        <button id="send-button" :disabled="!nick || !prompt" @click="sendMessage">Send</button>
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
      res_path: '', //production
      //res_path: 'http://localhost:80', //development
      rooms: [],
      room_id: 1,
      messages: [],
      nick: localStorage.getItem('nick'),
      prompt: '',
      new_msgs: 0,
    }
  },
  
  methods: {
    getRooms() {
      axios.get(`${this.res_path}/api/rooms`)
        .then(response => {
          this.rooms = response.data
        }).catch(error => {
          console.log(error)
        })
    },
    getMessages() {
      const old_len = this.messages.length
      axios.get(`${this.res_path}/api/messages/${this.room_id}`)
        .then(response => {
          this.messages = response.data
          if (this.messages.length > old_len) {
            setTimeout(() => {
              this.$refs.msglist.scrollTop = this.$refs.msglist.scrollHeight
            }, 10)
            if (document.hidden) {
              this.new_msgs += this.messages.length - old_len
              this.setFaviconBadge()
            }
          }
        }).catch(error => {
          console.log(error)
        })
    },
    sendMessage() {
      if (this.prompt.trim().length > 0) {
        axios.post(`${this.res_path}/api/messages/${this.room_id}`, {
          nick: this.nick,
          content: this.prompt
        })
          .then(response => {
            console.log(response.data)
            setTimeout(this.getMessages, 150)
          }).catch(error => {
            console.log(error)
          })
      }
      this.prompt = ''
    },
    setFaviconBadge() {
      var canvas = document.createElement("canvas")
      canvas.width = 16
      canvas.height = 16
      var ctx = canvas.getContext("2d")
      if (this.new_msgs) {
        ctx.fillStyle = "red"
      } else {
        ctx.fillStyle = "rgb(34,163,77)"
      }
      ctx.beginPath()
      ctx.arc(8, 8, 7, 0, Math.PI * 2, false)
      ctx.fill()
      if (this.new_msgs) {
        ctx.fillStyle = "white"
        ctx.font = "bold 10px sans-serif"
        ctx.fillText(this.new_msgs, 6, 11)
      }
      var link = document.querySelector("link[rel~='shortcut icon']")
      if (!link) {
        link = document.createElement("link")
        link.rel = "shortcut icon"
        document.head.appendChild(link)
      }
      link.type = "image/x-icon"
      link.href = canvas.toDataURL()
    },
    visChanged () {
      if (document.visibilityState === "visible") {
        this.new_msgs = 0
        this.setFaviconBadge()
        this.$refs.contentinput.focus()
      } 
    },
    storeNick () {
      localStorage.setItem('nick', this.nick)
    }
    
  },

  mounted() {
    this.setFaviconBadge()
    this.getRooms()
    this.getMessages()
    setInterval(this.getMessages, 1000)
    document.addEventListener("visibilitychange", this.visChanged)
  },

}
</script>

<style>
  body {
    font-family: Verdana, Geneva, Tahoma, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: greyscale;
  }
  #topbar {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 125px;
    background-color: #22a34d;
    border-radius: 10px;
  }
  #messagelist {
    position: fixed;
    top: 125px;
    width: calc(100% - 10px);
    bottom: 40px;
    overflow: auto;
  }
  #bottombar {
    position: fixed;
    bottom: 0;
    left: 0;
    width: 100%;
    height: 40px;
    background-color: rgb(34, 163, 77);
    border-radius: 10px;
  }
  #bottom-content {
    margin-top: 8px;
  }
  .whtxt {
    color: #fff;
  }
  label {
    padding: 15px;
    padding-right: 7px;
  }
  h1 {
    font-family:'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif;
    padding-left: 15px;
  }
  #content-input {
    width: 75%;
    border: none;
  }
  #nick-input {
    width: 150px;
  }
  #room-list {
    width: 150px;
  }
  #logo {
    position: fixed;
    top: 12px;
    right: 12px;
    border: solid 1px;
  }
  #send-button {
    font-family: Verdana, Geneva, Tahoma, sans-serif;
    margin-left: 10px;
    padding: 5px;
    background-color: #4fda7d;
    color: #fff;
    box-shadow: none;
    border: none;
    border-radius: 5px;
  }
  #send-button:disabled {
    background-color: #bbb;
  }
</style>
