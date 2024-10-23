import streamlit as st

class NewsCard:
    """Component for displaying cryptocurrency news"""
    
    def __init__(self):
        """Initialize NewsCard component"""
        pass
    
    def display(self, news_data):
        """
        Display news items with clickable headlines
        
        Args:
            news_data: DataFrame containing news with SOURCE, HEADLINE, and URL columns
        """
        st.subheader("📰 Latest Crypto News")
        
        if len(news_data) > 0:
            # Custom CSS for news items
            st.markdown("""
                <style>
                .news-source {
                    color: #666;
                    font-size: 0.8em;
                    margin-bottom: 2px;
                }
                .news-headline {
                    color: #2962FF;
                    text-decoration: none;
                    font-size: 0.95em;
                    line-height: 1.3;
                    font-weight: 500;
                }
                .news-headline:hover {
                    color: #1E40AF;
                    text-decoration: underline;
                }
                .news-item {
                    padding: 10px;
                    border-radius: 5px;
                    margin: 5px 0;
                    background-color: #f0f2f6;
                    border-left: 3px solid #2962FF;
                }
                </style>
            """, unsafe_allow_html=True)
            
            # Display each news item
            for _, news in news_data.iterrows():
                st.markdown(
                    f"""
                    <div class="news-item">
                        <div class="news-source">{news['SOURCE']}</div>
                        <a href="{news['URL']}" target="_blank" class="news-headline">
                            {news['HEADLINE']}
                        </a>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        else:
            st.info("No news available at the moment")
