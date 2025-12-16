// @ts-nocheck
/**
 * UserProfile - Class Component (Before Migration)
 * 
 * 📖 Book Reference: Chapter 7, Pattern 12 - Migration as Learning
 * 
 * This is the class-based version of the UserProfile component.
 * It demonstrates common patterns that need to be migrated to hooks.
 * 
 * NOTE: This is demonstration code. Run `npm install` to enable type checking.
 */

import React from 'react';

// Types
interface User {
  id: string;
  name: string;
  email: string;
  avatar: string;
  role: string;
  createdAt: string;
}

interface Props {
  userId: string;
  showDetails?: boolean;
  onUserLoad?: (user: User) => void;
}

interface State {
  loading: boolean;
  user: User | null;
  error: string | null;
}

// Mock API (replace with actual implementation)
const api = {
  getUser: async (userId: string): Promise<User> => {
    // Simulated API call
    return {
      id: userId,
      name: 'John Doe',
      email: 'john@example.com',
      avatar: 'https://example.com/avatar.jpg',
      role: 'Developer',
      createdAt: '2024-01-15',
    };
  },
};

// Components
const Spinner: React.FC = () => <div className="spinner">Loading...</div>;
const ErrorMessage: React.FC<{ message: string }> = ({ message }) => (
  <div className="error">{message}</div>
);

/**
 * UserProfile Class Component
 * 
 * Patterns used:
 * - Class state initialization
 * - componentDidMount for initial data fetch
 * - componentDidUpdate for prop changes
 * - componentWillUnmount for cleanup
 * - Class methods with arrow functions
 * - Conditional rendering
 */
class UserProfile extends React.Component<Props, State> {
  // State initialization using class property
  state: State = {
    loading: true,
    user: null,
    error: null,
  };

  // Track if component is mounted (for async safety)
  private mounted = false;

  // Lifecycle: Component mounted
  componentDidMount() {
    this.mounted = true;
    this.fetchUser();
  }

  // Lifecycle: Props changed
  componentDidUpdate(prevProps: Props) {
    // Refetch if userId changes
    if (prevProps.userId !== this.props.userId) {
      this.fetchUser();
    }
  }

  // Lifecycle: Component will unmount
  componentWillUnmount() {
    this.mounted = false;
  }

  // Async data fetching method
  fetchUser = async () => {
    const { userId, onUserLoad } = this.props;

    this.setState({ loading: true, error: null });

    try {
      const user = await api.getUser(userId);
      
      // Only update state if still mounted
      if (this.mounted) {
        this.setState({ loading: false, user });
        
        // Notify parent if callback provided
        if (onUserLoad) {
          onUserLoad(user);
        }
      }
    } catch (err) {
      if (this.mounted) {
        this.setState({
          loading: false,
          error: err instanceof Error ? err.message : 'Failed to load user',
        });
      }
    }
  };

  // Event handler method
  handleRefresh = () => {
    this.fetchUser();
  };

  // Render helper method
  renderUserDetails() {
    const { user } = this.state;
    const { showDetails } = this.props;

    if (!user || !showDetails) return null;

    return (
      <div className="user-details">
        <p>Email: {user.email}</p>
        <p>Role: {user.role}</p>
        <p>Member since: {user.createdAt}</p>
      </div>
    );
  }

  render() {
    const { loading, user, error } = this.state;

    // Loading state
    if (loading) {
      return <Spinner />;
    }

    // Error state
    if (error) {
      return (
        <div className="user-profile error-state">
          <ErrorMessage message={error} />
          <button onClick={this.handleRefresh}>Retry</button>
        </div>
      );
    }

    // No user found
    if (!user) {
      return <div className="user-profile">User not found</div>;
    }

    // Success state
    return (
      <div className="user-profile">
        <div className="user-header">
          <img src={user.avatar} alt={user.name} className="avatar" />
          <h2>{user.name}</h2>
        </div>
        
        {this.renderUserDetails()}
        
        <button onClick={this.handleRefresh}>Refresh</button>
      </div>
    );
  }
}

export default UserProfile;
export type { User, Props };
