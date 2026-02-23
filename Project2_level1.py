# STEP 1: Import libraries
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
import seaborn as sns

# STEP 2: Load your dataset (replace with actual file path if needed)
data = {
    'order_id': [1001, 1002, 1003, 1004, 1005, 1006, 1007],
    'order_status': ['shipped', 'shipped', 'cancelled', 'shipped', 'shipped', 'shipped', 'cancelled'],
    'order_source': ['website', 'whatsapp', 'website', 'website', 'website', 'whatsapp', 'website'],
    'order_date': ['2025-01-04', '2025-01-04', '2025-01-04', '2025-01-13', '2025-01-15', '2025-01-15', '2025-01-15'],
    'category': ['HNS', 'CK', 'CK', 'HNS', 'CK', 'HNS', 'Dng'],
    'sku': ['101-12', '101-12', 'Dng', 'Dng', 'Dng', '101-12', 'CK'],
    'quantity': [1, 2, 1, 3, 1, 2, 1],
    'sales': [1590, 2700, 1000, 3000, 1200, 2500, 900],
    'city': ['Karachi', 'Lahore', 'Karachi', 'Lahore', 'Islamabad', 'Karachi', 'Lahore']
}

df = pd.DataFrame(data)
df['order_date'] = pd.to_datetime(df['order_date'])

# STEP 3: Filter only shipped orders
df = df[df['order_status'] == 'shipped']

# STEP 4: Simulate customer ID
df['customer_id'] = df['order_source'] + '_' + df['city']

# STEP 5: Aggregate customer behavior
customer_summary = df.groupby('customer_id').agg(
    total_orders=('order_id', 'count'),
    total_sales=('sales', 'sum'),
    avg_order_value=('sales', 'mean'),
    total_quantity=('quantity', 'sum')
).reset_index()

# STEP 6: Normalize features
features = ['total_orders', 'total_sales', 'avg_order_value', 'total_quantity']
X = customer_summary[features]
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# STEP 7: Apply K-Means
kmeans = KMeans(n_clusters=2, random_state=42, n_init=10)
customer_summary['cluster'] = kmeans.fit_predict(X_scaled)

# STEP 8: Visualize clusters using PCA
pca = PCA(n_components=2)
pca_components = pca.fit_transform(X_scaled)
customer_summary['PCA1'] = pca_components[:, 0]
customer_summary['PCA2'] = pca_components[:, 1]

plt.figure(figsize=(8, 6))
sns.scatterplot(data=customer_summary, x='PCA1', y='PCA2', hue='cluster', palette='Set2', s=100)
plt.title('Customer Segmentation (PCA Projection)')
plt.xlabel('PCA Component 1')
plt.ylabel('PCA Component 2')
plt.grid(True)
plt.show()

# Optional: See clustered customer summary
print(customer_summary)
