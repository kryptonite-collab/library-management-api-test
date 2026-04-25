import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import DueReminderBanner from '../components/DueReminderBanner';

function MyHistory() {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [message, setMessage] = useState('');
  const [user, setUser] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    const userData = localStorage.getItem('user');
    if (userData) {
      try {
        setUser(JSON.parse(userData));
      } catch (e) {
        console.error('Failed to parse user data');
      }
    }
    fetchHistory();
  }, []);

  const fetchHistory = async () => {
    try {
      const token = localStorage.getItem('token');
      if (!token) {
        navigate('/login');
        return;
      }

      const response = await fetch('http://localhost:3001/api/reader/my-borrows', {
        headers: { 'Authorization': `Bearer ${token}` }
      });

      if (!response.ok) throw new Error('Failed to fetch');
      const data = await response.json();
      setHistory(data.loans || []);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleRenew = async (copyId) => {
    const token = localStorage.getItem('token');
    try {
      const response = await fetch('http://localhost:3001/api/reader/renew', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ copyId: copyId })
      });
      const data = await response.json();
      if (response.ok && data.success) {
        setMessage('续借成功！新截止日期: ' + new Date(data.newDueDate).toLocaleDateString());
        fetchHistory();
      } else {
        setMessage(data.message || '续借失败');
      }
    } catch (error) {
      setMessage('续借失败');
    }
    setTimeout(() => setMessage(''), 3000);
  };

  const handleReturn = async (loanId) => {
    const token = localStorage.getItem('token');
    try {
      const response = await fetch(`http://localhost:3001/api/reader/return/${loanId}`, {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${token}` }
      });
      const data = await response.json();
      if (response.ok) {
        setMessage('归还成功！');
        fetchHistory();
      } else {
        setMessage(data.message || '归还失败');
      }
    } catch (error) {
      setMessage('归还失败');
    }
    setTimeout(() => setMessage(''), 3000);
  };

  const getStatusText = (loan) => {
    if (loan.returnDate) return '已归还';
    const dueDate = new Date(loan.dueDate);
    if (dueDate < new Date()) return '已逾期';
    return '借阅中';
  };

  const getStatusColor = (loan) => {
    if (loan.returnDate) return 'bg-green-500';
    const dueDate = new Date(loan.dueDate);
    if (dueDate < new Date()) return 'bg-red-500';
    return 'bg-blue-500';
  };

  const canRenew = (loan) => {
    if (loan.returnDate) return false;
    const dueDate = new Date(loan.dueDate);
    if (dueDate < new Date()) return false;
    return (loan.renewCount || 0) < 2;
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    navigate('/login');
  };

  const getGreeting = () => {
    const hour = new Date().getHours();
    if (hour < 12) return '早上好';
    if (hour < 18) return '下午好';
    return '晚上好';
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <svg className="animate-spin h-8 w-8 text-blue-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
          <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
          <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
        </svg>
      </div>
    );
  }

  if (error) return (
    <div className="min-h-screen bg-gray-100">
      <header className="bg-white shadow-md sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-4 py-4 flex justify-between items-center">
          <div className="flex items-center gap-3">
            <div className="text-2xl">📚</div>
            <h1 className="text-xl font-bold text-gray-800">图书馆管理系统</h1>
            <span className="bg-green-100 text-green-600 text-xs px-2 py-1 rounded-full">读者</span>
          </div>
          <div className="flex items-center gap-4">
            <button onClick={handleLogout} className="bg-red-500 text-white px-4 py-2 rounded-lg hover:bg-red-600 transition text-sm">
              退出登录
            </button>
          </div>
        </div>
      </header>
      <div className="max-w-7xl mx-auto px-4 py-8">
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded-lg">
          错误: {error}
        </div>
      </div>
    </div>
  );

  return (
    <div className="min-h-screen bg-gray-100">
      <header className="bg-white shadow-md sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-4 py-4 flex justify-between items-center">
          <div className="flex items-center gap-3">
            <div className="text-2xl">📚</div>
            <h1 className="text-xl font-bold text-gray-800">图书馆管理系统</h1>
            <span className="bg-green-100 text-green-600 text-xs px-2 py-1 rounded-full">读者</span>
          </div>
          <div className="flex items-center gap-4">
            <div className="text-right">
              <p className="text-sm text-gray-500">{getGreeting()}</p>
              <p className="font-semibold text-gray-800">{user?.name || '读者'}</p>
              <p className="text-xs text-gray-400">{user?.email || ''}</p>
            </div>
            <button onClick={handleLogout} className="bg-red-500 text-white px-4 py-2 rounded-lg hover:bg-red-600 transition text-sm">
              退出登录
            </button>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 py-8">
        <DueReminderBanner />

        <div className="bg-gradient-to-r from-blue-500 to-purple-600 rounded-lg shadow-lg p-6 mb-8 text-white">
          <h2 className="text-2xl font-bold mb-2">{getGreeting()}，{user?.name || '读者'}！</h2>
          <p className="opacity-90">在这里您可以查看和管理您的借阅记录。</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div 
            onClick={() => navigate('/')}
            className="bg-white p-6 rounded-lg shadow-lg hover:shadow-xl transition cursor-pointer"
          >
            <div className="text-4xl mb-4">🔍</div>
            <h2 className="text-xl font-bold mb-2">图书搜索</h2>
            <p className="text-gray-500 text-sm mb-4">搜索并浏览图书</p>
            <button className="w-full bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600 transition">
              进入 →
            </button>
          </div>
          
          <div 
            onClick={() => navigate('/history')}
            className={`bg-white p-6 rounded-lg shadow-lg hover:shadow-xl transition cursor-pointer ${true ? 'ring-2 ring-blue-500' : ''}`}
          >
            <div className="text-4xl mb-4">📋</div>
            <h2 className="text-xl font-bold mb-2">借阅记录</h2>
            <p className="text-gray-500 text-sm mb-4">查看我的借阅历史</p>
            <button className="w-full bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600 transition">
              进入 →
            </button>
          </div>

          <div 
            onClick={() => navigate('/announcements')}
            className="bg-white p-6 rounded-lg shadow-lg hover:shadow-xl transition cursor-pointer"
          >
            <div className="text-4xl mb-4">📢</div>
            <h2 className="text-xl font-bold mb-2">公告通知</h2>
            <p className="text-gray-500 text-sm mb-4">查看图书馆公告</p>
            <button className="w-full bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600 transition">
              进入 →
            </button>
          </div>
        </div>

        {message && (
          <div className={`p-4 mb-6 rounded-lg ${message.includes('成功') ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'}`}>
            {message}
          </div>
        )}
        
        {history.length === 0 ? (
          <div className="bg-white rounded-lg shadow p-8 text-center text-gray-500">
            暂无借阅记录
          </div>
        ) : (
          <div className="bg-white rounded-lg shadow overflow-hidden">
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-gray-200">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">书名</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">作者</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">借阅日期</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">截止日期</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">归还日期</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">状态</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">操作</th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {history.map((loan) => (
                    <tr key={loan.id} className="hover:bg-gray-50">
                      <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{loan.copy?.book?.title || 'Unknown'}</td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{loan.copy?.book?.author || 'Unknown'}</td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{new Date(loan.checkoutDate).toLocaleDateString()}</td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{new Date(loan.dueDate).toLocaleDateString()}</td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{loan.returnDate ? new Date(loan.returnDate).toLocaleDateString() : '-'}</td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <span className={`px-2 py-1 text-xs font-medium text-white rounded-full ${getStatusColor(loan)}`}>
                          {getStatusText(loan)}
                        </span>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm">
                        {!loan.returnDate && (
                          <div className="flex gap-2">
                            {canRenew(loan) && (
                              <button
                                onClick={() => handleRenew(loan.copyId)}
                                className="px-2 py-1 bg-green-500 text-white text-xs rounded hover:bg-green-600 transition"
                              >
                                续借
                              </button>
                            )}
                            <button
                              onClick={() => handleReturn(loan.id)}
                              className="px-2 py-1 bg-red-500 text-white text-xs rounded hover:bg-red-600 transition"
                            >
                              归还
                            </button>
                          </div>
                        )}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}

export default MyHistory;
