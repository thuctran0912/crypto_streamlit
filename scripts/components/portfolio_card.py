import streamlit as st
import plotly.express as px
from ..utils.helpers import get_unique_key

class PortfolioCard:
    """Component for displaying portfolio performance"""
    
    def __init__(self):
        self.metrics_style = """
            <style>
            .portfolio-metric {
                padding: 10px;
                background-color: #f0f2f6;
                border-radius: 5px;
                margin: 5px 0;
            }
            .metric-label {
                font-size: 0.9em;
                color: #666;
            }
            .metric-value {
                font-size: 1.2em;
                font-weight: 500;
            }
            .positive {
                color: #059669;
            }
            .negative {
                color: #DC2626;
            }
            </style>
        """
    
    def create_holdings_chart(self, portfolio_data):
        """Create a pie chart of current holdings"""
        if len(portfolio_data) > 0:
            fig = px.pie(
                portfolio_data,
                values='current_value',
                names='SYMBOL',
                title='Portfolio Composition',
                hole=0.4
            )
            fig.update_layout(
                height=300,
                margin=dict(l=20, r=20, t=40, b=20)
            )
            return fig
        return None

    def display(self, portfolio_data, total_pl, total_value, overall_change):
        """
        Display portfolio performance and holdings
        
        Args:
            portfolio_data: DataFrame with portfolio details
            total_pl: Total profit/loss
            total_value: Total current value
            overall_change: Overall percentage change
        """
        st.subheader("💼 Portfolio Performance")
        
        # Add custom CSS
        st.markdown(self.metrics_style, unsafe_allow_html=True)
        
        # Create metrics layout
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(
                f"""
                <div class="portfolio-metric">
                    <div class="metric-label">Total Value</div>
                    <div class="metric-value">${total_value:,.2f}</div>
                </div>
                """,
                unsafe_allow_html=True
            )
            
        with col2:
            profit_class = "positive" if total_pl >= 0 else "negative"
            prefix = "+" if total_pl >= 0 else ""
            st.markdown(
                f"""
                <div class="portfolio-metric">
                    <div class="metric-label">Total Profit/Loss</div>
                    <div class="metric-value {profit_class}">{prefix}${total_pl:,.2f}</div>
                </div>
                """,
                unsafe_allow_html=True
            )
            
        with col3:
            change_class = "positive" if overall_change >= 0 else "negative"
            prefix = "+" if overall_change >= 0 else ""
            st.markdown(
                f"""
                <div class="portfolio-metric">
                    <div class="metric-label">Overall Change</div>
                    <div class="metric-value {change_class}">{prefix}{overall_change:.2f}%</div>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        # Display holdings chart
        if len(portfolio_data) > 0:
            holdings_fig = self.create_holdings_chart(portfolio_data)
            if holdings_fig:
                st.plotly_chart(holdings_fig, use_container_width=True, key=get_unique_key('holdings_chart'))
            
            # Display holdings table
            st.markdown("### Holdings Details")
            formatted_portfolio = portfolio_data.copy()
            formatted_portfolio['Current Value'] = formatted_portfolio['current_value'].map('${:,.2f}'.format)
            formatted_portfolio['Profit/Loss'] = formatted_portfolio['profit_loss'].map('${:,.2f}'.format)
            formatted_portfolio['Change'] = formatted_portfolio['percent_change'].map('{:+.2f}%'.format)
            
            display_columns = ['SYMBOL', 'QUANTITY', 'Current Value', 'Profit/Loss', 'Change']
            st.dataframe(
                formatted_portfolio[display_columns],
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("No portfolio data available")
