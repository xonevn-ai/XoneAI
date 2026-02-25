const { Agent, XoneAIAgents } = require('xoneai');

const researchAgent = new Agent({ instructions: 'Research about AI' });
const summariseAgent = new Agent({ instructions: 'Summarise research agent\'s findings' });

const agents = new XoneAIAgents({ agents: [researchAgent, summariseAgent] });
agents.start();
