/**
 * Gateway/Bot Module for XoneAI TypeScript SDK
 * 
 * Python parity with xoneaiagents gateway/bot types
 * 
 * Provides:
 * - Bot protocols and interfaces
 * - Gateway protocols and interfaces
 * - Message types
 */

// ============================================================================
// Bot Types
// ============================================================================

/**
 * Bot configuration.
 * Python parity: xoneaiagents/bots
 */
export interface BotConfig {
  name: string;
  token?: string;
  prefix?: string;
  channels?: string[];
  allowedUsers?: string[];
  metadata?: Record<string, any>;
}

/**
 * Bot user.
 * Python parity: xoneaiagents/bots
 */
export interface BotUser {
  id: string;
  name: string;
  displayName?: string;
  isBot?: boolean;
  metadata?: Record<string, any>;
}

/**
 * Bot channel.
 * Python parity: xoneaiagents/bots
 */
export interface BotChannel {
  id: string;
  name: string;
  type: 'text' | 'voice' | 'dm' | 'group';
  metadata?: Record<string, any>;
}

/**
 * Bot message.
 * Python parity: xoneaiagents/bots
 */
export interface BotMessage {
  id: string;
  content: string;
  author: BotUser;
  channel: BotChannel;
  timestamp: Date;
  attachments?: Array<{
    url: string;
    type: string;
    name?: string;
  }>;
  metadata?: Record<string, any>;
}

/**
 * Bot protocol interface.
 * Python parity: xoneaiagents/bots
 */
export interface BotProtocol {
  name: string;
  config: BotConfig;
  
  connect(): Promise<void>;
  disconnect(): Promise<void>;
  
  sendMessage(channel: string, content: string): Promise<BotMessage>;
  onMessage(handler: (message: BotMessage) => void | Promise<void>): void;
  
  getUser(userId: string): Promise<BotUser | null>;
  getChannel(channelId: string): Promise<BotChannel | null>;
}

// ============================================================================
// Gateway Types
// ============================================================================

/**
 * Gateway configuration.
 * Python parity: xoneaiagents/gateway
 */
export interface GatewayConfig {
  url: string;
  apiKey?: string;
  timeout?: number;
  retryAttempts?: number;
  retryDelay?: number;
  metadata?: Record<string, any>;
}

/**
 * Gateway event.
 * Python parity: xoneaiagents/gateway
 */
export interface GatewayEvent {
  type: string;
  data: any;
  timestamp: Date;
  source?: string;
  metadata?: Record<string, any>;
}

/**
 * Gateway message.
 * Python parity: xoneaiagents/gateway
 */
export interface GatewayMessage {
  id: string;
  type: 'request' | 'response' | 'event' | 'error';
  payload: any;
  timestamp: Date;
  correlationId?: string;
  metadata?: Record<string, any>;
}

/**
 * Gateway protocol interface.
 * Python parity: xoneaiagents/gateway
 */
export interface GatewayProtocol {
  config: GatewayConfig;
  
  connect(): Promise<void>;
  disconnect(): Promise<void>;
  isConnected(): boolean;
  
  send(message: GatewayMessage): Promise<void>;
  receive(): Promise<GatewayMessage | null>;
  
  onEvent(handler: (event: GatewayEvent) => void | Promise<void>): void;
  onError(handler: (error: Error) => void): void;
}

/**
 * Gateway client protocol.
 * Python parity: xoneaiagents/gateway
 */
export interface GatewayClientProtocol extends GatewayProtocol {
  request(payload: any, timeout?: number): Promise<any>;
  subscribe(eventType: string, handler: (event: GatewayEvent) => void): () => void;
}

/**
 * Gateway session protocol.
 * Python parity: xoneaiagents/gateway
 */
export interface GatewaySessionProtocol {
  sessionId: string;
  userId?: string;
  startTime: Date;
  metadata?: Record<string, any>;
  
  isActive(): boolean;
  extend(duration: number): void;
  terminate(): void;
}

// ============================================================================
// Provider Status
// ============================================================================

/**
 * Provider status.
 * Python parity: xoneaiagents/gateway
 */
export interface ProviderStatus {
  name: string;
  status: 'online' | 'offline' | 'degraded' | 'unknown';
  latency?: number;
  lastCheck: Date;
  errorCount?: number;
  metadata?: Record<string, any>;
}

// ============================================================================
// Failover Types
// ============================================================================

/**
 * Failover configuration.
 * Python parity: xoneaiagents/gateway
 */
export interface FailoverConfig {
  providers: string[];
  strategy: 'round-robin' | 'priority' | 'random' | 'least-latency';
  maxRetries?: number;
  retryDelay?: number;
  healthCheckInterval?: number;
}

/**
 * Failover manager.
 * Python parity: xoneaiagents/gateway
 */
export class FailoverManager {
  private config: FailoverConfig;
  private providerStatuses: Map<string, ProviderStatus> = new Map();
  private currentIndex: number = 0;

  constructor(config: FailoverConfig) {
    this.config = config;
    
    // Initialize provider statuses
    for (const provider of config.providers) {
      this.providerStatuses.set(provider, {
        name: provider,
        status: 'unknown',
        lastCheck: new Date(),
      });
    }
  }

  /**
   * Get the next provider based on strategy.
   */
  getNextProvider(): string | null {
    const availableProviders = this.config.providers.filter(p => {
      const status = this.providerStatuses.get(p);
      return status?.status !== 'offline';
    });

    if (availableProviders.length === 0) {
      return null;
    }

    switch (this.config.strategy) {
      case 'round-robin':
        this.currentIndex = (this.currentIndex + 1) % availableProviders.length;
        return availableProviders[this.currentIndex];
      
      case 'priority':
        return availableProviders[0];
      
      case 'random':
        return availableProviders[Math.floor(Math.random() * availableProviders.length)];
      
      case 'least-latency':
        let minLatency = Infinity;
        let bestProvider = availableProviders[0];
        for (const provider of availableProviders) {
          const status = this.providerStatuses.get(provider);
          if (status?.latency !== undefined && status.latency < minLatency) {
            minLatency = status.latency;
            bestProvider = provider;
          }
        }
        return bestProvider;
      
      default:
        return availableProviders[0];
    }
  }

  /**
   * Update provider status.
   */
  updateStatus(provider: string, status: Partial<ProviderStatus>): void {
    const current = this.providerStatuses.get(provider);
    if (current) {
      this.providerStatuses.set(provider, {
        ...current,
        ...status,
        lastCheck: new Date(),
      });
    }
  }

  /**
   * Mark provider as failed.
   */
  markFailed(provider: string): void {
    this.updateStatus(provider, {
      status: 'offline',
      errorCount: (this.providerStatuses.get(provider)?.errorCount ?? 0) + 1,
    });
  }

  /**
   * Mark provider as healthy.
   */
  markHealthy(provider: string, latency?: number): void {
    this.updateStatus(provider, {
      status: 'online',
      latency,
      errorCount: 0,
    });
  }

  /**
   * Get all provider statuses.
   */
  getStatuses(): ProviderStatus[] {
    return Array.from(this.providerStatuses.values());
  }
}

// ============================================================================
// Auth Types
// ============================================================================

/**
 * Auth profile.
 * Python parity: xoneaiagents/auth
 */
export interface AuthProfile {
  userId: string;
  username?: string;
  email?: string;
  roles?: string[];
  permissions?: string[];
  token?: string;
  expiresAt?: Date;
  metadata?: Record<string, any>;
}

// ============================================================================
// Resource Limits
// ============================================================================

/**
 * Resource limits.
 * Python parity: xoneaiagents/limits
 */
export interface ResourceLimits {
  maxTokens?: number;
  maxRequests?: number;
  maxConcurrent?: number;
  rateLimitPerMinute?: number;
  rateLimitPerHour?: number;
  maxMemoryMB?: number;
  maxExecutionTimeMs?: number;
}

// ============================================================================
// Sandbox Types
// ============================================================================

/**
 * Sandbox status.
 * Python parity: xoneaiagents/sandbox
 */
export enum SandboxStatus {
  IDLE = 'idle',
  RUNNING = 'running',
  COMPLETED = 'completed',
  FAILED = 'failed',
  TIMEOUT = 'timeout',
}

/**
 * Sandbox result.
 * Python parity: xoneaiagents/sandbox
 */
export interface SandboxResult {
  status: SandboxStatus;
  output?: string;
  error?: string;
  exitCode?: number;
  duration?: number;
  metadata?: Record<string, any>;
}

/**
 * Sandbox protocol.
 * Python parity: xoneaiagents/sandbox
 */
export interface SandboxProtocol {
  execute(code: string, language?: string): Promise<SandboxResult>;
  executeFile(filePath: string): Promise<SandboxResult>;
  terminate(): Promise<void>;
  getStatus(): SandboxStatus;
}

// ============================================================================
// Autonomy Types
// ============================================================================

/**
 * Autonomy level.
 * Python parity: xoneaiagents/autonomy
 */
export enum AutonomyLevel {
  NONE = 'none',
  SUGGEST = 'suggest',
  AUTO_APPROVE = 'auto_approve',
  FULL_AUTO = 'full_auto',
}

// ============================================================================
// Reflection Types
// ============================================================================

/**
 * Reflection output.
 * Python parity: xoneaiagents/reflection
 */
export interface ReflectionOutput {
  originalOutput: string;
  reflectedOutput: string;
  iterations: number;
  improvements: string[];
  score?: number;
  metadata?: Record<string, any>;
}

// ============================================================================
// RAG Types
// ============================================================================

/**
 * RAG retrieval policy.
 * Python parity: xoneaiagents/rag
 */
export enum RagRetrievalPolicy {
  SIMILARITY = 'similarity',
  MMR = 'mmr',
  HYBRID = 'hybrid',
  RERANK = 'rerank',
}

// ============================================================================
// Auto RAG Types
// ============================================================================

/**
 * Auto RAG configuration.
 * Python parity: xoneaiagents/knowledge
 */
export interface AutoRagConfig {
  sources: string[];
  chunkSize?: number;
  chunkOverlap?: number;
  topK?: number;
  rerank?: boolean;
  retrievalPolicy?: RagRetrievalPolicy;
}
