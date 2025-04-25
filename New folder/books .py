import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from wordcloud import WordCloud

st.set_page_config(layout="wide")
st.title("📚 Book Store Data Dashboard")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("C:/Users/Sama Naser/Downloads/cleaned_books_data.csv")   
    return df

df = load_data()

# Tabs
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["📊 General Analysis", "🏆 Best & Worst Books", "📦 Availability & Description", "☁️ Word Cloud", "📖 Book Details", "📑 Book Analytics"])

# ----- 📊 General Analysis -----
with tab1:
    # 💰 Cheapest book by rating
    st.header("💰 Cheapest Book by Rating")
    cheapest_by_rating = df.loc[df.groupby('Rating')['Price'].idxmin()][['Title', 'Price', 'Rating']]
    fig1, ax1 = plt.subplots(figsize=(10, 6))
    sns.barplot(data=cheapest_by_rating, x='Rating', y='Price', hue='Title', ax=ax1)
    ax1.set_title('Cheapest Book by Rating')
    if ax1.get_legend() is not None:
        ax1.get_legend().set_visible(False)  # Remove legend
    st.pyplot(fig1)

    # Display data in table
    st.subheader("Data for Cheapest Book by Rating")
    st.dataframe(cheapest_by_rating)

    # 💰 Cheapest book by category
    st.header("💰 Cheapest Book by Category")
    cheapest_by_category = df.loc[df.groupby('Category')['Price'].idxmin()][['Title', 'Price', 'Category']]
    fig2, ax2 = plt.subplots(figsize=(12, 6))
    sns.barplot(data=cheapest_by_category, x='Category', y='Price', hue='Title', ax=ax2)
    ax2.set_title('Cheapest Book by Category')
    if ax2.get_legend() is not None:
        ax2.get_legend().set_visible(False)  # Remove legend
    plt.xticks(rotation=90)
    st.pyplot(fig2)

    # Display data in table
    st.subheader("Data for Cheapest Book by Category")
    st.dataframe(cheapest_by_category)

    # 📊 Top 10 Categories
    st.header("📊 Top 10 Categories")
    top_categories = df['Category'].value_counts().head(10)
    fig3, ax3 = plt.subplots(figsize=(10, 6))
    top_categories.plot(kind='bar', color='skyblue', ax=ax3)
    ax3.set_title('Top 10 Categories by Number of Books')
    st.pyplot(fig3)

    # Display data in table
    st.subheader("Data for Top 10 Categories")
    top_categories_df = top_categories.reset_index()
    top_categories_df.columns = ['Category', 'Number of Books']
    st.dataframe(top_categories_df)

    # 📊 Number of Books per Rating - Pie Chart
    st.header("📊 Number of Books per Rating")
    books_per_rating = df['Rating'].value_counts().sort_index()  # Count the books per rating
    fig4, ax4 = plt.subplots(figsize=(8, 8))  # Create a larger figure for the pie chart
    ax4.pie(books_per_rating.values, labels=books_per_rating.index, autopct='%1.1f%%', colors=sns.color_palette('Set3', len(books_per_rating)))
    ax4.set_title('Number of Books per Rating')
    st.pyplot(fig4)


# ----- 🏆 Best & Worst Books -----
with tab2:
    # 🏆 Highest Rated Book
    st.header("🏆 Highest Rated Book")
    best_book = df.loc[df['Rating'].idxmax()]
    st.success(f"{best_book['Title']}\n\n"
               f"⭐ Rating: {best_book['Rating']}\n\n"
               f"💰 Price: {best_book['Price']}\n\n"
               f"📂 Category: {best_book['Category']}")

    # 🌟 Best Book by Category
    st.header("🌟 Best Book by Category")
    best_per_category = df.loc[df.groupby('Category')['Rating'].idxmax()][['Title', 'Rating', 'Category', 'Price']]
    fig4, ax4 = plt.subplots(figsize=(12, 6))
    sns.barplot(data=best_per_category, x='Category', y='Rating', hue='Title', ax=ax4)
    ax4.set_title('Best Rated Book by Category')
    if ax4.get_legend() is not None:
        ax4.get_legend().set_visible(False)   
    plt.xticks(rotation=90)
    st.pyplot(fig4)

    # Display data in table
    st.subheader("Data for Best Book by Category")
    st.dataframe(best_per_category)

    # 😞 Lowest Rated Book
    st.header("😞 Lowest Rated Book")
    worst_book = df.loc[df['Rating'].idxmin()]
    st.error(f"{worst_book['Title']}\n\n"
             f"⭐ Rating: {worst_book['Rating']}\n\n"
             f"💰 Price: {worst_book['Price']}\n\n"
             f"📂 Category: {worst_book['Category']}")

# ----- 📦 Availability & Description -----
with tab3:
    # 📦 Most Available Books
    st.header("📦 Most Available Books")
    book_availability = df[['Title', 'Available_Quantity']].sort_values(by='Available_Quantity', ascending=False)
    fig5, ax5 = plt.subplots(figsize=(12, 6))
    sns.barplot(data=book_availability.head(20), x='Available_Quantity', y='Title', palette='viridis', ax=ax5)
    ax5.set_title('Top 20 Books by Availability')
    if ax5.get_legend() is not None:
        ax5.get_legend().set_visible(False)   
    st.pyplot(fig5)

    # Display data in table
    st.subheader("Data for Most Available Books")
    st.dataframe(book_availability.head(20))

    # 📝 Random Book Description
    st.header("📝 Random Book Description")
    random_book = df.sample(1).iloc[0]
    st.markdown(f"### {random_book['Title']}")
    st.write(random_book['Description'])

# ----- ☁️ Word Cloud -----
with tab4:
    st.header("☁️ Word Cloud from Book Descriptions")
    text = " ".join(df['Description'].dropna().astype(str).tolist())
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
    fig6, ax6 = plt.subplots(figsize=(12, 6))
    ax6.imshow(wordcloud, interpolation='bilinear')
    ax6.axis('off')
    st.pyplot(fig6)

# ----- 📖 Book Details -----
with tab5:
    st.subheader("📖 Book Details")
    selected_book = st.selectbox("Select a Book to View Details", df['Title'].unique())
    book_info = df[df['Title'] == selected_book].iloc[0]

    st.markdown(f"""
    ### {book_info['Title']}
    **⭐ Rating:** {book_info['Rating']}  
    **💰 Price:** {book_info['Price']}  
    **📂 Category:** {book_info['Category']}  
    **📦 Available:** {book_info['Available_Quantity']} copies  
    **🔗 Book Link:** [Click here to visit the link]({book_info['Link']})
    """)

    with st.expander("📄 Full Description"):
        st.write(book_info['Description'])

# ----- 📑 Book Details & Analytics -----
with tab6:
    st.subheader("📑 Book Analytics")
    
    # عدد الكتب حسب الفئة
    st.header("📚 Number of Books per Category")
    books_per_category = df['Category'].value_counts()
    st.bar_chart(books_per_category)

    # عدد الكتب حسب التقييم
    st.header("📊 Number of Books per Rating")
    books_per_rating = df['Rating'].value_counts().sort_index()
    st.bar_chart(books_per_rating)

    # وصف عام للبيانات
    st.header("📑 Data Description")
    st.write("Here is a brief overview of the data:")
    st.write(f"Total number of books: {df.shape[0]}")
    st.write(f"Number of unique categories: {df['Category'].nunique()}")
    st.write(f"Average price: {df['Price'].mean():.2f}")
    st.write(f"Highest price: {df['Price'].max()}")
    st.write(f"Lowest price: {df['Price'].min()}")
    st.write(f"Average rating: {df['Rating'].mean():.2f}")
    st.write(f"Highest rating: {df['Rating'].max()}")
    st.write(f"Lowest rating: {df['Rating'].min()}")

    # مقارنة الأسعار حسب الفئات
    st.header("💰 Price Comparison by Category")
    avg_price_per_category = df.groupby('Category')['Price'].mean().sort_values(ascending=False)
    st.bar_chart(avg_price_per_category)

    # توزيع عدد الكتب المتاحة
    st.header("📦 Books Availability Distribution")
    availability_dist = df['Available_Quantity'].describe()
    st.write(availability_dist)

 
